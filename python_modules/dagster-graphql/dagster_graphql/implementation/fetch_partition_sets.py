import yaml
from graphql.execution.base import ResolveInfo

from dagster import check
from dagster.api.snapshot_partition import (
    sync_get_external_partition_config,
    sync_get_external_partition_names,
    sync_get_external_partition_tags,
)
from dagster.core.host_representation import (
    ExternalPartitionConfigData,
    ExternalPartitionNamesData,
    ExternalPartitionSet,
    ExternalPartitionTagsData,
    RepositoryHandle,
    RepositorySelector,
)

from .utils import capture_dauphin_error


def get_partition_sets_or_error(graphene_info, repository_selector, pipeline_name):
    check.inst_param(graphene_info, 'graphene_info', ResolveInfo)
    check.inst_param(repository_selector, 'repository_selector', RepositorySelector)
    check.str_param(pipeline_name, 'pipeline_name')
    location = graphene_info.context.get_repository_location(repository_selector.location_name)
    repository = location.get_repository(repository_selector.repository_name)
    partition_sets = [
        partition_set
        for partition_set in repository.get_external_partition_sets()
        if partition_set.pipeline_name == pipeline_name
    ]

    return graphene_info.schema.type_named('PartitionSets')(
        results=[
            graphene_info.schema.type_named('PartitionSet')(
                external_repository_handle=repository.handle, external_partition_set=partition_set,
            )
            for partition_set in sorted(
                partition_sets,
                key=lambda partition_set: (
                    partition_set.pipeline_name,
                    partition_set.mode,
                    partition_set.name,
                ),
            )
        ]
    )


@capture_dauphin_error
def get_partition_set(graphene_info, repository_selector, partition_set_name):
    check.inst_param(graphene_info, 'graphene_info', ResolveInfo)
    check.inst_param(repository_selector, 'repository_selector', RepositorySelector)
    check.str_param(partition_set_name, 'partition_set_name')
    location = graphene_info.context.get_repository_location(repository_selector.location_name)
    repository = location.get_repository(repository_selector.repository_name)
    partition_sets = repository.get_external_partition_sets()
    for partition_set in partition_sets:
        if partition_set.name == partition_set_name:
            return graphene_info.schema.type_named('PartitionSet')(
                external_repository_handle=repository.handle, external_partition_set=partition_set,
            )

    return graphene_info.schema.type_named('PartitionSetNotFoundError')(partition_set_name)


@capture_dauphin_error
def get_partition_by_name(graphene_info, repository_handle, partition_set, partition_name):
    check.inst_param(graphene_info, 'graphene_info', ResolveInfo)
    check.inst_param(repository_handle, 'repository_handle', RepositoryHandle)
    check.inst_param(partition_set, 'partition_set', ExternalPartitionSet)
    check.str_param(partition_name, 'partition_name')
    return graphene_info.schema.type_named('Partition')(
        external_repository_handle=repository_handle,
        external_partition_set=partition_set,
        partition_name=partition_name,
    )


def get_partition_config_yaml(
    _graphene_info, repository_handle, partition_set_name, partition_name
):
    check.inst_param(repository_handle, 'repository_handle', RepositoryHandle)
    check.str_param(partition_set_name, 'partition_set_name')
    check.str_param(partition_name, 'partition_name')
    result = sync_get_external_partition_config(
        repository_handle, partition_set_name, partition_name
    )
    if isinstance(result, ExternalPartitionConfigData):
        return yaml.dump(result.run_config, default_flow_style=False)
    else:
        # TODO: surface user-facing error here, using the serialized error
        # https://github.com/dagster-io/dagster/issues/2576
        return ''


def get_partition_tags(graphene_info, repository_handle, partition_set_name, partition_name):
    check.inst_param(repository_handle, 'repository_handle', RepositoryHandle)
    check.str_param(partition_set_name, 'partition_set_name')
    check.str_param(partition_name, 'partition_name')
    result = sync_get_external_partition_tags(repository_handle, partition_set_name, partition_name)
    if isinstance(result, ExternalPartitionTagsData):
        return [
            graphene_info.schema.type_named('PipelineTag')(key=key, value=value)
            for key, value in result.tags.items()
        ]
    else:
        # TODO: surface user-facing error here, using the serialized error
        # https://github.com/dagster-io/dagster/issues/2576
        return []


def get_partitions(
    graphene_info, repository_handle, partition_set, cursor=None, limit=None, reverse=False
):
    check.inst_param(repository_handle, 'repository_handle', RepositoryHandle)
    check.inst_param(partition_set, 'partition_set', ExternalPartitionSet)
    result = sync_get_external_partition_names(repository_handle, partition_set.name)

    if isinstance(result, ExternalPartitionNamesData):
        partition_names = _apply_cursor_limit_reverse(
            result.partition_names, cursor, limit, reverse
        )

        return graphene_info.schema.type_named('Partitions')(
            results=[
                graphene_info.schema.type_named('Partition')(
                    external_partition_set=partition_set,
                    external_repository_handle=repository_handle,
                    partition_name=partition_name,
                )
                for partition_name in partition_names
            ]
        )

    else:
        # TODO: surface user-facing error here, using the serialized error
        # https://github.com/dagster-io/dagster/issues/2576
        return []


def _apply_cursor_limit_reverse(items, cursor, limit, reverse):
    start = 0
    end = len(items)
    index = 0

    if cursor:
        index = next((idx for (idx, item) in enumerate(items) if item == cursor), None)

        if reverse:
            end = index
        else:
            start = index + 1

    if limit:
        if reverse:
            start = end - limit
        else:
            end = start + limit

    return items[start:end]
