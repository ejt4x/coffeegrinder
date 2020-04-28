#!/usr/bin/env python

# vim: bg=dark

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START pubsub_quickstart_sub_all]
import argparse
import os
import json
from google.auth import jwt
from grinder import CoffeeGrinder

# [START pubsub_quickstart_sub_deps]
from google.cloud import pubsub_v1

# [END pubsub_quickstart_sub_deps]


def sub(project_id, subscription_name):
    """Receives messages from a Pub/Sub subscription."""

    service_account_info = json.load(open("apikey.json"))
    audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
    credentials = jwt.Credentials.from_service_account_info(
                
    service_account_info, audience=audience
                )

    subscriber_client = pubsub_v1.SubscriberClient(credentials=credentials)

    # [END pubsub_quickstart_sub_client]
    # Create a fully qualified identifier in the form of
    # `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber_client.subscription_path(
        project_id, subscription_name
    )
    grinder = CoffeeGrinder()

    def callback(message):
        print(
            "Received message {} of message ID {}\n".format(
                message, message.message_id
            )
        )
        # Acknowledge the message. Unack'ed messages will be redelivered.
        message.ack()
        print("Acknowledged message {}\n".format(message.message_id))
        if message.data == 'GRIND' or message.data == b"GRIND" :
            print("Grind message received")
            try: 
                grind_time = int(message.attributes["time"])
            except:
                print("No grind time received")
                grind_time = None
                return
               
            print("Grind time requested: {} seconds".format(grind_time))
            grinder.timed_grind(grind_time)
        else:
            print("Unable to handle this message")
            

    streaming_pull_future = subscriber_client.subscribe(
        subscription_path, callback=callback
    )

    print("Listening for messages on {}..\n".format(subscription_path))

    try:
        # Calling result() on StreamingPullFuture keeps the main thread from
        # exiting while messages get processed in the callbacks.
        streaming_pull_future.result()
    except Exception as e:  # noqa
        print(e)
        streaming_pull_future.cancel()
        grinder.cleanup()

    subscriber_client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    subscription_name = os.getenv('SUBSCRIPTION_NAME')

    args = parser.parse_args()

    sub(project_id, subscription_name)
# [END pubsub_quickstart_sub_all]

