import asyncio

from integrations.calendly import service as calendly_service


def test_list_event_types_handles_boolean_mock_mode_setting():
    original_mock_mode = calendly_service.settings.calendly_mock_mode
    original_token = calendly_service.settings.calendly_personal_access_token

    try:
        calendly_service.settings.calendly_mock_mode = True
        calendly_service.settings.calendly_personal_access_token = ""

        event_types = asyncio.run(calendly_service.list_event_types())
    finally:
        calendly_service.settings.calendly_mock_mode = original_mock_mode
        calendly_service.settings.calendly_personal_access_token = original_token

    assert event_types == calendly_service.FALLBACK_EVENT_TYPES
