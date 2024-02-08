'''
Template Component main class.

'''

import logging

from keboola.component import ComponentBase
from keboola.component.exceptions import UserException
from keboola.csvwriter import ElasticDictWriter

from pyzoom import ZoomClient, refresh_tokens

# configuration variables
STATE_REFRESH_TOKEN = "#refresh_token"
KEY_WEBINAR_ID = 'webinar_id'


# #### Keep for debug
KEY_STDLOG = 'stdlogging'
KEY_DEBUG = 'debug'
MANDATORY_PARS = []
MANDATORY_IMAGE_PARS = []

APP_VERSION = '0.1.0'


class Component(ComponentBase):

    def __init__(self, debug=False):
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
        '''
        Main execution code
        '''

        webinar_ids = self.configuration.parameters.get(KEY_WEBINAR_ID, None)
        if not webinar_ids:
            raise UserException(f"[ERROR] Webinar IDs is not provided.")

        out_table = self.create_out_table_definition('registrants.csv')

        with ElasticDictWriter(out_table.full_path, out_table.columns) as writer:

            for web_id in webinar_ids:

                extracted_registrants = 0
                try:
                    registered_res = self.client.raw.get_all_pages("/webinars/" + web_id + "/registrants")

                    for registrant in registered_res.get('registrants', []):
                        writer.writerow(registrant)
                        extracted_registrants += 1

                except Exception as e:
                    logging.error(f"[ERROR] When obtaining details of webinar: {web_id} failed with error: {e} ")

            logging.info(f"[INFO] Extracted {extracted_registrants} registrants from webinar: {web_id}")

        self.write_manifest(out_table)


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
