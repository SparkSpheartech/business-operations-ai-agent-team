# Copyright 2025 Google LLC
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

"""Unit tests for tools"""

from unittest.mock import MagicMock, patch

from google.adk.tools import ToolContext

from brand_search_optimization.tools import bq_connector
from brand_search_optimization.shared_libraries import constants


class TestBrandSearchOptimization:

    @patch("brand_search_optimization.tools.bq_connector.client")
    def test_get_business_details(self, mock_client):
        # Mock ToolContext
        mock_tool_context = MagicMock(spec=ToolContext)
        
        output = bq_connector.get_business_details(mock_tool_context)
        assert "Spark Sphear Tech Solutions" in output

    def test_create_task_roadmap(self):
        goal = "Launch AI Agent"
        output = bq_connector.create_task_roadmap(goal)
        assert f"Roadmap for {goal}" in output
        assert "Onyx" in output
        assert "Travis" in output
        assert "Eissa" in output
