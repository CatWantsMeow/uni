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

import { Injectable } from '@angular/core';
import { Router } from "@angular/router"
import { Http, Response, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

@Injectable()
export class DataService<Type> {
    private resolveSuffix = '?resolve=true';
    private actionUrl: string;
    private headers: Headers;

    constructor(public router: Router, private http: Http) {
        this.actionUrl = '/api/';
        this.headers = new Headers();
        this.headers.append('Content-Type', 'application/json');
        this.headers.append('Accept', 'application/json');
    }

    public getAll(ns: string): Observable<Type[]> {
        var token = this.checkLogin()
        if (token == null) {
            return Observable.throw("Unauthorized");
        }
        console.log('GetAll ' + ns + ' to ' + this.actionUrl + ns);
        return this.http.get(`${this.actionUrl}${ns}/?access_token=${token}`)
          .map(this.extractData)
          .catch(this.handleError);
    }

    public getSingle(ns: string, id: string): Observable<Type> {
        var token = this.checkLogin()
        if (token == null) {
            return Observable.throw("Unauthorized");
        }

        console.log('GetSingle ' + ns);

        return this.http.get(this.actionUrl + ns + '/' + id + this.resolveSuffix + '&access_token=' + token)
          .map(this.extractData)
          .catch(this.handleError);
    }

    public add(ns: string, asset: Type): Observable<Type> {
        var token = this.checkLogin()
        if (token == null) {
            return Observable.throw("Unauthorized");
        }

        console.log('Entered DataService add');
        console.log('Add ' + ns);
        console.log('asset', asset);

        return this.http.post(this.actionUrl + ns + '?access_token=' + token, asset)
          .map(this.extractData)
          .catch(this.handleError);
    }

    public update(ns: string, id: string, itemToUpdate: Type): Observable<Type> {
        var token = this.checkLogin()
        if (token == null) {
            return Observable.throw("Unauthorized");
        }

        console.log('Update ' + ns);
        console.log('what is the id?', id);
        console.log('what is the updated item?', itemToUpdate);
        console.log('what is the updated item?', JSON.stringify(itemToUpdate));

        return this.http.put(`${this.actionUrl}${ns}/${id}/?access_token=${token}`, itemToUpdate)
          .map(this.extractData)
          .catch(this.handleError);
    }

    public delete(ns: string, id: string): Observable<Type> {
        var token = this.checkLogin()
        if (token == null) {
            return Observable.throw("Unauthorized");
        }
        console.log('Delete ' + ns);

        return this.http.delete(this.actionUrl + ns + '/' + id + '/?access_token=' + token)
          .map(this.extractData)
          .catch(this.handleError);
    }

    public login(ns: string, data: Type): Observable<Type> {
        console.log('login', JSON.stringify(data));

        return this.http.post(`/proxy/auth/`, data)
          .map(this.setUserData)
          .catch(this.handleError);
    }

    private setUserData(res: Response): any {
        var data = res.json();
        localStorage.setItem('userToken', data.token);
        localStorage.setItem('userId', data.id);
        localStorage.setItem('userClass', data.class);
    }

    private checkLogin() {
        var userToken = localStorage.getItem('userToken');
        if (userToken == null) {
            this.router.navigate(['/Login'])
        }
        return userToken
    }

    private handleError(error: any): Observable<string> {
        // In a real world app, we might use a remote logging infrastructure
        // We'd also dig deeper into the error to get a better message

        // if (error.status == 401 && !window.location.href.includes('/Login')) {
        //     console.log('Redirecting from', window.location.href)
        //     window.location.replace('/Login')
        // }

        const errMsg = (error.message) ? error.message :
          error.status ? `${error.status} - ${error.statusText}` : 'Server error';
        console.error(errMsg); // log to console instead
        return Observable.throw(errMsg);
    }

    private extractData(res: Response): any {
        return res.json();
    }
}
