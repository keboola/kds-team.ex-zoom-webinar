"""
Template Component main class.

"""

import logging

from keboola.component.base import ComponentBase, sync_action
from keboola.component.exceptions import UserException
from keboola.csvwriter import ElasticDictWriter
from keboola.component.sync_actions import SelectElement


from pyzoom import ZoomClient, refresh_tokens

# configuration variables
STATE_REFRESH_TOKEN = "#refresh_token"
KEY_WEBINAR_ID = 'webinar_id'
KEY_ENDPOINTS = 'endpoints'

APP_VERSION = '0.2.0'


class Component(ComponentBase):

    def __init__(self):
        super().__init__()

        if not self.configuration.oauth_credentials:
            raise UserException("The configuration is not authorized. Please authorize the configuration first.")

        authorization = self.configuration.oauth_credentials
        refresh_token = self.get_state_file().get(STATE_REFRESH_TOKEN, [])

        if refresh_token:
            logging.info("Refresh token loaded from state file")
        else:
            refresh_token = authorization.data.get("refresh_token")

        refreshed_tokens = refresh_tokens(authorization['appKey'], authorization['appSecret'], refresh_token)

        self.write_state_file({STATE_REFRESH_TOKEN: refreshed_tokens.get("refresh_token")})
        self.client = ZoomClient(refreshed_tokens.get("access_token"), refreshed_tokens.get("refresh_token"))

    def run(self):
        """
        Main execution code
        """

        logging.info(f"[INFO] Running Zoom Webinar Extractor v{APP_VERSION}")

        webinar_id = self.configuration.parameters.get(KEY_WEBINAR_ID, None)
        if not webinar_id:
            raise UserException(f"[ERROR] Webinar IDs is not provided.")

        endpoints = self.configuration.parameters.get(KEY_ENDPOINTS, None)

        for endpoint in endpoints:
            self.extract_data(webinar_id, endpoint)

    def extract_data(self, webinar_id: str, endpoint: str) -> None:
        """
        Extracts data from Zoom API and writes it to the output table.

        Args:
            webinar_id: id of the webinar to extract data from
            endpoint: endpoint to extract data from

        """

        extracted_records = 0
        try:
            response = self.client.raw.get_all_pages("/webinars/" + webinar_id + "/" + endpoint)

            results = response.get(endpoint, [])

            if results:
                out_table = self.create_out_table_definition(f'{endpoint.replace("/", "-")}.csv')

                with ElasticDictWriter(out_table.full_path, out_table.columns) as writer:

                    for row in results:
                        writer.writerow(row)
                        extracted_records += 1

                out_table = self.create_out_table_definition(f'{endpoint.replace("/", "-")}.csv',
                                                             columns=writer.fieldnames)

                self.write_manifest(out_table)

        except Exception as e:
            logging.error(f"[ERROR] When obtaining {endpoint} of webinar: {webinar_id} failed with error: {e} ")

        logging.info(f"[INFO] Extracted {extracted_records} {endpoint} from webinar: {webinar_id}")

    @sync_action('get_webinars')
    def get_webinars(self):

        try:
            result = self.client.raw.get_all_pages("/users/me/webinars")
            webinars = result.get('webinars', [])

        except Exception as client_exc:
            raise UserException(client_exc) from client_exc

        return [SelectElement(value=(str(wbn["id"])), label=f'{wbn["topic"]} ({str(wbn["id"])})') for wbn in webinars]


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
