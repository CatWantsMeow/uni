/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { Component, OnInit, Input, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';
import { LoginService } from './Login.service';
import 'rxjs/add/operator/toPromise';

@Component({
  selector: 'app-login',
  templateUrl: './Login.component.html',
  styleUrls: ['./Login.component.css'],
  providers: [LoginService]
})
@Injectable()
export class LoginComponent {

  myForm: FormGroup;
  private participant;
  private errorMessage;

  username = new FormControl('', Validators.required);
  password = new FormControl('', Validators.required);

  constructor(public serviceLogin: LoginService, fb: FormBuilder, private router: Router) {
    this.myForm = fb.group({
      username: this.username,
      password: this.password
    });
  };

  login(form: any): Promise<any> {
    this.participant = {
      'username': this.username.value,
      'password': this.password.value
    };

    this.myForm.setValue({
      'username': null,
      'password': null
    });

    return this.serviceLogin.login(this.participant)
    .toPromise()
    .then(() => {
      this.errorMessage = null;
      this.myForm.setValue({
        'username': null,
        'password': null
      });
      window.location.href = '/';
      // this.router.navigate(['/'])
    })
    .catch((error) => {
      if (error === 'Server error') {
        this.errorMessage = 'Could not connect to REST server. Please check your configuration details';
      } else {
        this.errorMessage = error;
      }
    });
  }

  resetForm(): void {
    this.myForm.setValue({
      'username': null,
      'password': null
    });
  }
}
