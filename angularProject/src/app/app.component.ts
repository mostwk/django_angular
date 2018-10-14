import {Component, OnInit} from '@angular/core';
import {register} from "ts-node";
import {UserService} from "./user.service";
import {HttpErrorResponse} from "@angular/common/http";
import {BlogPostService} from "./blog-post.service";
import {throwError} from "rxjs/internal/observable/throwError";

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
  public posts;
  public new_post: any;


  constructor(private userService: UserService, private blogPostService: BlogPostService) {

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
    this.getPosts();
    this.new_post = {};

  }
  registerUser() {
  this.userService.registerNewUser(this.input).subscribe(
    response => {
      alert("User" + this.input.username + "has been created successfully");
      this.input.password = '';
      this.input.confirmed_password = '';
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
        this.token = response.token;
        this.user.username = this.input.username;
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

  getPosts(){
    this.blogPostService.list().subscribe(
      data => {
        this.posts = data;
        for (let post of this.posts){
          post.date = new Date(post.date)
        }
      },
      error => console.error(error),
      () => console.log('Done loading posts')
    );
  }

  createPost(){
    this.new_post['author'] = this.user.username;
     this.blogPostService.create(this.new_post).subscribe(
       data => {
         console.log(this.new_post);
         this.getPosts();
         return true;
       },
       error => {
         console.log('Error saving new post');
         return throwError(error);
       }
     )
    }
}
