import {Component, OnInit} from '@angular/core';
import {register} from "ts-node";
import {UserService} from "./user.service";
import {HttpErrorResponse} from "@angular/common/http";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [UserService]
})


export class AppComponent implements OnInit {
  input;
  public token: string;
  public user: any;


  constructor(private userService: UserService) {

  }
  ngOnInit() {
    this.input = {
      username: "",
      password: "",
      confirmed_password: "",
      email: ""
    };
    this.user = {
      username: '',
      password: ''
    };
    this.token = "";
  }
  registerUser() {
  this.userService.registerNewUser(this.input).subscribe(
    response => {
      alert("User" + this.input.username + "has been created successfully");
    },
    HttpErrorResponse => {
      alert(HttpErrorResponse.error.message);
      console.log("error", HttpErrorResponse);
    }
  );
  }

  loginUser() {
    this.userService.loginUser(this.input).subscribe(
      response => {
        console.log(response);
        this.token = response.token;
        this.user.username = this.input.username;
        alert("User " + this.input.username + " logged in ");
      },
      error => {
        console.log("error", error);
        this.input.username = '';
        this.input.password = '';
        this.input.confirmed_password = '';
      }
    );
  }
  logoutUser() {
    this.token = null;
    this.user.username = null;
    this.input.password = '';
    this.input.confirmed_password = '';
  }
}
