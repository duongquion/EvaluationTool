
from django.db import models
from api.models import TimeStamped, UserTrackable

class CriteriaRoleEnum(models.TextChoices):
    TL = "TL", "Team Lead"
    MB = "MB", "Member"


class CriteriaVersionStateEnum(models.TextChoices):
    UNOFFICIAL = "Unofficial", "Unofficial"
    OFFICIAL = "Official", "Official"
    OUTDATED = "Outdated", "Outdated"


class CriteriaVersion(TimeStamped, UserTrackable):
    version_name = models.CharField(
        max_length=200, unique=True, 
        verbose_name='Version Name'
    )
    role_name = models.CharField(
        max_length=2, 
        choices=CriteriaRoleEnum.choices, 
        default=CriteriaRoleEnum.MB,
        help_text="Role that this criteria tree version is implemented to",
        verbose_name='Role name'
    )
    state = models.CharField(
        max_length=32,
        choices=CriteriaVersionStateEnum.choices,
        default=CriteriaVersionStateEnum.UNOFFICIAL,
        help_text="Criteria tree version state",
    )

    def __str__(self):
        return self.version_name


class ResultPolicy(models.Model):
    version = models.OneToOneField(
        CriteriaVersion,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    grading_rule = models.JSONField(
        help_text="Define perfomance point to grade mapping",
        verbose_name='Grading rule'
    )
    action_grades = models.JSONField(
        help_text="Grades need to take action",
        verbose_name='Action grades'
    )
    explanation_grades = models.JSONField(
        help_text="Grades need to be explained",
        verbose_name='Explanation grades'
    )

    def __str__(self):
        return f"{self.version}"

    class Meta:
        verbose_name_plural = "Result policies"


class InputType(models.Model):
    name = models.CharField(
        max_length=20, 
        help_text="Input type name",
        unique=True,
    )
    min = models.IntegerField(
        null=True,
        blank=True,
        help_text="Minimum value of the input type (if this is None => negative infinity)",
    )
    max = models.IntegerField(
        null=True,
        blank=True,
        help_text="Maximum value of the input type (if this is None => positive infinity)",
    )

    def __str__(self):
        return self.name


class Criteria(models.Model):
    version = models.ForeignKey(
        CriteriaVersion, 
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
    )
    alias = models.CharField(
        max_length=20,
        help_text="Alias for this criteria (used for creating expression)",
    )
    parent_alias = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Parent criteria alias of this criteria (null if this criteria has no parent)",
        verbose_name='Parent alias'
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="A description for this criteria",
    )
    is_input = models.BooleanField(
        default=False,
        help_text="Is this criteria an input criteria (if this true, it will not be counted in the evaluation calculating)",
        verbose_name='Is input'
    )
    input_type = models.ForeignKey(
        InputType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Type of Input value (% or #), if this is None, using the default value type (negative infinity to positive infinity)",
        verbose_name='Input type'
    )
    expression = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="The expression to calculate evaluation point",
    )
    is_final_result = models.BooleanField(
        default=False,
        help_text="Criteria will be used to get the final result",
        verbose_name='Is final result'
    )

    def __str__(self):
        return f"{self.version}_{self.alias}_{self.name}"

    class Meta:
        verbose_name_plural = "Criteria"


class VariableRelationship(models.Model):
    version = models.ForeignKey(
        CriteriaVersion, 
        on_delete=models.CASCADE,
    )
    from_alias = models.CharField(
        max_length=20,
        help_text="Select the variable (alias) that this relationship depends on",
        verbose_name='From'
    )
    to_alias = models.CharField(
        max_length=20,
        help_text="Select the variable (alias) that depends on this relationship",
        verbose_name='To'
    )

    def __str__(self):
        return f"{self.version}: {self.from_alias} -> {self.to_alias}"
