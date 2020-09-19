from django.contrib import admin


def get_app_index(app_list: list, app_label: str) -> int:
    for i, app in enumerate(app_list):
        if app.get("app_label") == app_label:
            return i


class SiteAdmin(admin.AdminSite):
    site_header = "DomePortfolio Administration"
    index_title = "DomePortfolio Administration"
    site_title = "Administration"

    admin_app_ordering = {
        "auth": ("users", "auth"),
        "categories": ("categories",),
        "content": ("content",),
        "portfolio": ("portfolio",),
        "shop": ("shop", "orders"),
    }

    @staticmethod
    def _merge_apps(toplevel_app: dict,
                    mergees: list) -> dict:
        new_app = toplevel_app
        for app in mergees:
            new_app["models"] += app.get("models")
        return new_app

    def _assemble_app_dict(self,
                           app_list: list,
                           app_label: str) -> dict:
        original_app = app_list[
            get_app_index(app_list, app_label)
        ]
        additional_app_labels = self.admin_app_ordering.get(app_label, tuple())
        if additional_app_labels:
            additional_app_labels = tuple(
                i for i in additional_app_labels if not i == app_label
            )
        apps_to_merge = [
            app_list[
                get_app_index(app_list, a)
            ] for a in additional_app_labels
        ]
        return self._merge_apps(original_app, apps_to_merge)

    def get_app_list(self, request):
        """ Overrides the app_list based on the admin_app_ordering parameter """
        app_list = super(SiteAdmin, self).get_app_list(request)
        # Do not process if the attribute has not been set
        if not self.admin_app_ordering:
            return app_list
        # If we are at the login site
        if request.user.id is None:
            return app_list

        new_app_list = []
        for original_app_label, additional_app_labels in self.admin_app_ordering.items():
            # This means we need to make changes to the app_dict
            if len(additional_app_labels) > 1:
                new_app_list.append(
                    self._assemble_app_dict(
                        app_list, original_app_label
                    )
                )

            # In this case the app_dict is fine as it is
            else:
                new_app_list.append(
                    app_list[get_app_index(app_list, original_app_label)]
                )

        return new_app_list
