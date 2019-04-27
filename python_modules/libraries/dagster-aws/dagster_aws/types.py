from enum import Enum as PyEnum

from dagster import Enum, EnumValue

from dagster.core.types.runtime import Stringish
from dagster.utils import safe_isfile


class FileExistsAtPath(Stringish):
    def __init__(self):
        super(FileExistsAtPath, self).__init__(description='A path at which a file actually exists')

    def coerce_runtime_value(self, value):
        value = super(FileExistsAtPath, self).coerce_runtime_value(value)
        return self.throw_if_false(safe_isfile, value)


EbsVolumeType = Enum(
    name='EbsVolumeType', enum_values=[EnumValue('gp2'), EnumValue('io1'), EnumValue('standard')]
)


class EmrClusterState(PyEnum):
    Starting = 'STARTING'
    Bootstrapping = 'BOOTSTRAPPING'
    Running = 'RUNNING'
    Waiting = 'WAITING'
    Terminating = 'TERMINATING'
    Terminated = 'TERMINATED'
    TerminatedWithErrors = 'TERMINATED_WITH_ERRORS'


EmrActionOnFailure = Enum(
    name='EmrActionOnFailure',
    enum_values=[
        EnumValue('TERMINATE_JOB_FLOW'),
        EnumValue('TERMINATE_CLUSTER'),
        EnumValue('CANCEL_AND_WAIT'),
        EnumValue('CONTINUE'),
    ],
)

EmrAdjustmentType = Enum(
    name='EmrAdjustmentType',
    enum_values=[
        EnumValue('CHANGE_IN_CAPACITY'),
        EnumValue('PERCENT_CHANGE_IN_CAPACITY'),
        EnumValue('EXACT_CAPACITY'),
    ],
)

EmrComparisonOperator = Enum(
    name='EmrComparisonOperator',
    enum_values=[
        EnumValue('GREATER_THAN_OR_EQUAL'),
        EnumValue('GREATER_THAN'),
        EnumValue('LESS_THAN'),
        EnumValue('LESS_THAN_OR_EQUAL'),
    ],
)

EmrInstanceRole = Enum(
    name='EmrInstanceRole', enum_values=[EnumValue('MASTER'), EnumValue('CORE'), EnumValue('TASK')]
)

EmrMarket = Enum(name='EmrMarket', enum_values=[EnumValue('ON_DEMAND'), EnumValue('SPOT')])

EmrRepoUpgradeOnBoot = Enum(
    name='EmrRepoUpgradeOnBoot', enum_values=[EnumValue('SECURITY'), EnumValue('NONE')]
)

EmrScaleDownBehavior = Enum(
    name='EmrScaleDownBehavior',
    enum_values=[
        EnumValue('TERMINATE_AT_INSTANCE_HOUR'),
        EnumValue('TERMINATE_AT_TASK_COMPLETION'),
    ],
)

EmrStatistic = Enum(
    name='EmrStatistic',
    enum_values=[
        EnumValue('SAMPLE_COUNT'),
        EnumValue('AVERAGE'),
        EnumValue('SUM'),
        EnumValue('MINIMUM'),
        EnumValue('MAXIMUM'),
    ],
)

EmrSupportedProducts = Enum(
    name='EmrSupportedProducts', enum_values=[EnumValue('mapr-m3'), EnumValue('mapr-m5')]
)

EmrTimeoutAction = Enum(
    name='EmrTimeoutAction',
    enum_values=[EnumValue('SWITCH_TO_ON_DEMAND'), EnumValue('TERMINATE_CLUSTER')],
)

EmrUnit = Enum(
    name='EmrUnit',
    enum_values=[
        EnumValue('NONE'),
        EnumValue('SECONDS'),
        EnumValue('MICRO_SECONDS'),
        EnumValue('MILLI_SECONDS'),
        EnumValue('BYTES'),
        EnumValue('KILO_BYTES'),
        EnumValue('MEGA_BYTES'),
        EnumValue('GIGA_BYTES'),
        EnumValue('TERA_BYTES'),
        EnumValue('BITS'),
        EnumValue('KILO_BITS'),
        EnumValue('MEGA_BITS'),
        EnumValue('GIGA_BITS'),
        EnumValue('TERA_BITS'),
        EnumValue('PERCENT'),
        EnumValue('COUNT'),
        EnumValue('BYTES_PER_SECOND'),
        EnumValue('KILO_BYTES_PER_SECOND'),
        EnumValue('MEGA_BYTES_PER_SECOND'),
        EnumValue('GIGA_BYTES_PER_SECOND'),
        EnumValue('TERA_BYTES_PER_SECOND'),
        EnumValue('BITS_PER_SECOND'),
        EnumValue('KILO_BITS_PER_SECOND'),
        EnumValue('MEGA_BITS_PER_SECOND'),
        EnumValue('GIGA_BITS_PER_SECOND'),
        EnumValue('TERA_BITS_PER_SECOND'),
        EnumValue('COUNT_PER_SECOND'),
    ],
)
