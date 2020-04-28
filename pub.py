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

# [START pubsub_quickstart_pub_all]
import time
import os
import json

# [START pubsub_quickstart_pub_deps]
from google.cloud import pubsub_v1

# [END pubsub_quickstart_pub_deps]

def get_callback(api_future, data, ref):
    """Wrap message data in the context of the callback function."""

    def callback(api_future):
        try:
            print(
                "Published message {} now has message ID {}".format(
                    data, api_future.result()
                )
            )
            ref["num_messages"] += 1
        except Exception:
            print(
                    "A problem occurred when publishing {}: {}\n".format(
                    data, api_future.exception()
                )
            )
            raise

    return callback


def pub(project_id, topic_name, grind_time=None):
    """Publishes a message to a Pub/Sub topic."""
    # [START pubsub_quickstart_pub_client]
    # Initialize a Publisher client.
    client = pubsub_v1.PublisherClient()
    # [END pubsub_quickstart_pub_client]
    # Create a fully qualified identifier in the form of
    # `projects/{project_id}/topics/{topic_name}`
    topic_path = client.topic_path(project_id, topic_name)

    # Data sent to Cloud Pub/Sub must be a bytestring.
    data = b"GRIND"

    # Keep track of the number of published messages.
    ref = dict({"num_messages": 0})

    # When you publish a message, the client returns a future.
    if grind_time is not None:
        api_future = client.publish(topic_path, data=data, time=str(int(grind_time)))
    else:
        api_future = client.publish(topic_path, data=data)
    api_future.add_done_callback(get_callback(api_future, data, ref))

    # Keep the main thread from exiting while the message future
    # gets resolved in the background.
    while api_future.running():
        time.sleep(0.5)
        print("Published {} message(s).".format(ref["num_messages"]))

def grind(grind_time=None):
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    topic_name = os.getenv('SUBSCRIPTION_NAME')

    pub(project_id, topic_name, grind_time)
    


if __name__ == "__main__":

    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    topic_name = os.getenv('SUBSCRIPTION_NAME')

    pub(project_id, topic_name, 2)
# [END pubsub_quickstart_pub_all]

