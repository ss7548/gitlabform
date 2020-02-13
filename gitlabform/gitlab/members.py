from gitlabform.gitlab.core import GitLabCore


class GitLabMembers(GitLabCore):

    def add_member_to_project(self, project_and_group_name, username, access_level, expires_at=None):
        data = {
            "user_id": self._get_user_id(username),
            "expires_at": expires_at
        }
        if access_level is not None:
            data['access_level'] = access_level

        # 409 means that the user is already a member of the project, so let's accept it for idempotency
        return self._make_requests_to_api("projects/%s/members", project_and_group_name, method='POST',
                                          data=data, expected_codes=[201, 409])

    def remove_member_from_project(self, project_and_group_name, user):
        # 409 means that the user is already not a member of the project, so let's accept it for idempotency
        return self._make_requests_to_api("projects/%s/members/%s", (project_and_group_name, self._get_user_id(user)),
                                          method='DELETE', expected_codes=[204, 404])

    def get_group_members(self, group_name, all=False):
        url_template = "groups/%s/members"
        if all:
            url_template += "/all"

        return self._make_requests_to_api(url_template, group_name)

    def add_member_to_group(self, group_name, username, access_level, expires_at=None):
        data = {
            "user_id": self._get_user_id(username),
            "expires_at": expires_at
        }
        if access_level is not None:
            data['access_level'] = access_level

        # 409 means that the user is already a member of the group, so let's accept it for idempotency
        return self._make_requests_to_api("groups/%s/members", group_name, method='POST',
                                          data=data, expected_codes=[201, 409])

    def remove_member_from_group(self, group_name, user):
        # 403 means that we are trying to remove creator from the group which is not possible
        # 404 means that the user is already removed, so let's accept it for idempotency
        return self._make_requests_to_api("groups/%s/members/%s", (group_name, self._get_user_id(user)),
                                          method='DELETE', expected_codes=[204, 403, 404])
