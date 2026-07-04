from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AuthorOrModeratorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()

        return (
            obj.author == self.request.user
            or self.request.user.is_moderator
        )
