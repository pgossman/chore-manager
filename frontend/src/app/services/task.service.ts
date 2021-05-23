import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Person } from '../Person';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  }),
};

@Injectable({
  providedIn: 'root',
})
export class TaskService {
  private apiUrl = 'http://localhost:5000/people';
  constructor(private http: HttpClient) {}

  getAllChores(): Observable<Person[]> {
    return this.http.get<Person[]>(this.apiUrl);
  }

  getMyChores(name: string): Observable<Person> {
    // TODO: FIX URL, RETURNS EMPTY OBJ ATM
    const url = `${this.apiUrl}/${name}`;
    return this.http.get<Person>(url);
  }
}
