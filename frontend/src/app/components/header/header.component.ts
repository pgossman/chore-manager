import { Component, Input, OnInit } from '@angular/core';
import { Person } from 'src/app/Person';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent implements OnInit {
  title: string = 'Chore Manager';
  @Input() name: string;
  constructor() {}

  ngOnInit(): void {}

  onSubmit() {
    // if (!this.text) {
    //   alert('Please add a task!');
    // }
    console.log('name: ' + this.name);
  }
}
