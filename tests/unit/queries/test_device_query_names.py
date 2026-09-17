"""Validate the required name field for device-scoped audit queries."""

import jq


def test_device_queries_emit_non_empty_unique_names(query_data, load_fixture):
    """Every emitted device resource has a stable top-level name."""
    modules = sorted(
        module_fqcn
        for module_fqcn in query_data
        if module_fqcn.startswith("cisco.meraki.devices_")
    )

    for module_fqcn in modules:
        response = load_fixture(module_fqcn)
        assert response is not None, f"Fixture {module_fqcn}.json not found"
        final_response = (
            response
            if "meraki_response" in response
            else {"meraki_response": response}
        )
        results = jq.compile(query_data[module_fqcn]["query"]).input(final_response).all()

        for result_batch in results:
            assert isinstance(result_batch, list), module_fqcn
            names = [item.get("name") for item in result_batch]
            assert all(names), f"Missing name in {module_fqcn}: {result_batch}"
            assert len(names) == len(set(names)), (
                f"Duplicate names in {module_fqcn}: {names}"
            )
