import { Component, Input, OnInit } from '@angular/core';
import { Person } from 'src/app/Person';

@Component({
  selector: 'app-task-item',
  templateUrl: './task-item.component.html',
  styleUrls: ['./task-item.component.css'],
})
export class TaskItemComponent implements OnInit {
  @Input() person: Person;
  constructor() {}

  ngOnInit(): void {}

  submitTask(): void {
    console.log('submitted task');
  }
}
