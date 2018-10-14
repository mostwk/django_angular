import { Injectable } from '@angular/core';
import { HttpClient} from "@angular/common/http";
import { UserService} from "./user.service";

@Injectable({
  providedIn: 'root'
})
export class BlogPostService {

  constructor(private http: HttpClient, private userService: UserService) {
  }
    list(){
      return this.http.get('http://127.0.0.1:8000/api/posts/')
    }

    create(post){
      return this.http.post('http://127.0.0.1:8000/api/posts/', post)
    }

}
