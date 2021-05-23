import { Component, OnInit } from '@angular/core';
import { TaskService } from 'src/app/services/task.service';
import { Person } from '../../Person';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.css'],
})
export class TasksComponent implements OnInit {
  people: Person[] = [];
  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.taskService.getChores().subscribe((people) => (this.people = people));
  }
}
