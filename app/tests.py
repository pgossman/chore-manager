from typing import Callable

from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    Chore,
    ChoreAssignment,
    ChoreInstance,
    DayOfWeek,
    PartOfDay,
    ChoreStatus,
)


class InstanceProcessTests(TestCase):
    USER1_NAME = "johnny"
    USER1_PASS = "abc123"

    USER2_NAME = "grace"
    USER2_PASS = "def123987"

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create_user(
            username=self.USER1_NAME,
            email=f"{self.USER1_NAME}@rocket.gov",
            password=self.USER1_PASS,
        )

        self.user2 = User.objects.create_user(
            username=self.USER2_NAME,
            email=f"{self.USER2_NAME}@rocket.gov",
            password=self.USER2_PASS,
        )

    def _login_user1(self) -> None:
        assert self.client.login(username=self.USER1_NAME, password=self.USER1_PASS)

    def _login_user2(self) -> None:
        assert self.client.login(username=self.USER2_NAME, password=self.USER2_PASS)

    def _create_chore(self, name: str) -> Chore:
        return Chore.objects.create(name=name)

    def _create_assignment(
        self, user: User, chore: Chore, dow: DayOfWeek, time: PartOfDay
    ) -> ChoreAssignment:
        assignment = ChoreAssignment.objects.create(chore=chore, dow=dow, time=time,)
        assignment.users.add(user)
        assignment.save()

        return assignment

    def _create_instance(
        self, user: User, assignment: ChoreAssignment
    ) -> ChoreInstance:
        return ChoreInstance.objects.create(
            user=user,
            assignment=assignment,
            status=ChoreStatus.ASSIGNED,
            due_date=timezone.now(),
        )

    def _get_content(self, url: str) -> str:
        response = self.client.get(url)

        return response.content.decode("utf-8")

    def test_view_assignments_on_homepage(self):
        self._login_user1()

        chore1_name = "sweep kitchen floors"
        dow1 = DayOfWeek.MONDAY
        time1 = PartOfDay.AFTERNOON

        chore2_name = "dishes"
        dow2 = DayOfWeek.TUESDAY
        time2 = PartOfDay.EVENING

        chore1 = self._create_chore(chore1_name)
        chore2 = self._create_chore(chore2_name)

        self._create_assignment(self.user1, chore1, dow1, time1)
        self._create_assignment(self.user1, chore2, dow2, time2)

        content = self._get_content("/")
        self.assertTrue(f"{chore1_name} {dow1.label} {time1.label}" in content)
        self.assertTrue(f"{chore2_name} {dow2.label} {time2.label}" in content)

    def test_view_instances_on_homepage(self):
        self._login_user1()

        # TODO: add multiple instances
        chore_name = "sweep kitchen floors"
        dow = DayOfWeek.MONDAY
        time = PartOfDay.AFTERNOON

        chore = self._create_chore(chore_name)
        assignment = self._create_assignment(self.user1, chore, dow, time)

        # Creating an instance gives the user the option to submit
        self.assertTrue("No chores available for submission" in self._get_content("/"))
        instance = self._create_instance(self.user1, assignment)
        self.assertFalse("No chores available for submission" in self._get_content("/"))
        self.assertTrue("Submit a chore" in self._get_content("/"))

        # New instance is marked as assigned
        self.assertEqual(ChoreStatus.ASSIGNED, instance.status)

    def test_submit_assigned_instance(self):
        self._login_user1()

        chore_name = "sweep kitchen floors"
        dow = DayOfWeek.MONDAY
        time = PartOfDay.AFTERNOON

        chore = self._create_chore(chore_name)
        assignment = self._create_assignment(self.user1, chore, dow, time)
        instance = self._create_instance(self.user1, assignment)

        self.assertEqual(ChoreStatus.ASSIGNED, instance.status)

        instance_notes = "Hello sorry its a little late"
        self.client.post(
            "/instance/submit", {"instance": instance.id, "notes": instance_notes}
        )

        # Submitted chore is marked as submitted, notes are attached
        instance = ChoreInstance.objects.filter(id=instance.id).get()
        self.assertEqual(ChoreStatus.SUBMITTED, instance.status)
        self.assertEqual(instance_notes, instance.notes)

    def test_review_submitted_instance(self):
        pass
