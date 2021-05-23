import { Component, Input, OnInit } from '@angular/core';
import { TaskService } from 'src/app/services/task.service';
import { Person } from '../../Person';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.css'],
})
export class TasksComponent implements OnInit {
  people: Person[] = [];
  @Input() person: Person;
  me: Person;
  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.taskService
      .getAllChores()
      .subscribe((people) => (this.people = people));
  }

  getMyChores(name: string) {
    this.taskService
      .getMyChores(name)
      .subscribe(
        () => (this.me = this.people.filter((t) => t.name === name)[0])
      );
  }
}
