from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib import messages

from account.models import User
from .models import Project, UserProject
from .forms import UserProjectReviewRequestForm


class ProjectList(ListView):
    queryset = Project.objects.active()


class ProjectDetail(DetailView):
    def get_object(self):
        """
        We need to find object by using `pk` and `slug`.
        """
        return get_object_or_404(
            Project,
            pk=self.kwargs.get('pk'),
            slug=self.kwargs.get('slug'),
            status=Project.STATUS_ACTIVE
        )

    def post(self, request, slug, pk):
        user = request.user
        project = self.get_object()

        next_url = reverse('projects:detail', args=[slug, pk])
        # not authenticated, ask for login
        if not user.is_authenticated:
            messages.warning(
                request,
                'Silahkan login terlebih dahulu sebelum mengerjakan proyek.',
                extra_tags='warning'
            )
            return HttpResponseRedirect(reverse('account:login') + '?next={}'.format(next_url))

        # assign user to the project
        _, created = project.assign_to(user)
        if created:
            messages.info(request,
                          "Selamat mengerjakan `{}`!".format(project.title),
                          extra_tags='success')
        success_url = reverse('projects:detail_user', args=[
                              slug, pk, user.username])
        return HttpResponseRedirect(success_url)


class ProjectDetailUser(DetailView):
    template_name = 'projects/project_detail_user.html'

    def get_object(self):
        """
        We need to find object by using `pk` and `slug`.
        """
        return get_object_or_404(
            Project,
            pk=self.kwargs.get('pk'),
            slug=self.kwargs.get('slug'),
            status=Project.STATUS_ACTIVE
        )

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        user_project = get_object_or_404(
            UserProject, user=user, project=self.object)

        data = super().get_context_data(**kwargs)
        data['user_project'] = user_project

        # show completion form only when:
        # - requirements completed
        # - url has `?form=1`
        # - current user is the owner
        rev_request = self.request.GET.get('form') == '1'
        show_rr_form = user_project.is_requirements_complete() \
            and rev_request \
            and (user == self.request.user)

        if show_rr_form:
            data['rr_form'] = UserProjectReviewRequestForm(
                instance=user_project)
        return data

    def __handle_update(self, request, project, user_project):
        """
        Handle requirements status changes.
        """
        redirect_url = reverse('projects:detail_user', args=[
            project.slug, project.pk, request.user.username])

        requirements = user_project.requirements
        if requirements:
            # create a copy and modify this instead so we can compare it later
            requirements_copy = requirements.copy()

            # update requirements_copy
            updated_reqs = map(lambda r: int(r),
                               request.POST.getlist('reqs', []))

            # remove `complete` flag
            for r in requirements_copy:
                if r.get('complete'):
                    del r['complete']

            # assign new flag from `updated_reqs`
            for index in updated_reqs:
                req = requirements_copy[index]
                req['complete'] = True

            # save changes
            user_project.requirements = requirements_copy
            user_project.calculate_progress()
            user_project.save()

            # if all requirements completed, ready for review
            if user_project.is_requirements_complete():
                messages.info(request,
                              "Mantap! Proyek kamu siap untuk direview. Klik tombol `Review Request`",
                              extra_tags='success')

        return HttpResponseRedirect(redirect_url)

    def __handle_review_request(self, request, project, user_project):
        form = UserProjectReviewRequestForm(
            request.POST, instance=user_project)

        if form.is_valid():
            review_requested = form.submit_review()
            if review_requested:
                messages.info(request,
                              "Great job! Proyek kamu sudah disubmit untuk direview team UpKoding.",
                              extra_tags='success')
            else:
                messages.info(request,
                              "Detail proyek berhasil diupdate!",
                              extra_tags='success')
            return HttpResponse()
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json; charset=utf-8')

    def post(self, request, slug, pk, username):
        user = request.user
        request_kind = request.POST.get('kind')
        project_url = reverse('projects:detail', args=[slug, pk])

        # not loggedin?
        if (not user.is_authenticated):
            return HttpResponseRedirect(project_url)

        project = self.get_object()
        user_project = get_object_or_404(
            UserProject, user=user, project=project)

        if request_kind == 'update':
            return self.__handle_update(request, project, user_project)

        if request_kind == 'delete':
            user_project.delete()
            messages.info(request,
                          "Proyek `{}` telah dibatalkan :(".format(
                              project.title),
                          extra_tags='warning')
            return HttpResponse()

        if request_kind == 'review_request':
            return self.__handle_review_request(request, project, user_project)
        return HttpResponseRedirect(project_url)
