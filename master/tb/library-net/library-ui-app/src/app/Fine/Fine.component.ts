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

import { Component, OnInit, Input } from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';
import { FineService } from './Fine.service';
import 'rxjs/add/operator/toPromise';

@Component({
  selector: 'app-fine',
  templateUrl: './Fine.component.html',
  styleUrls: ['./Fine.component.css'],
  providers: [FineService]
})
export class FineComponent implements OnInit {

  myForm: FormGroup;

  private allAssets;
  private asset;
  private currentId;
  private errorMessage;

  public currentUserId;
  public currentUserClass;
  public isReader;
  public isLibrarian;
  public isSupplier;

  id = new FormControl('', Validators.required);
  size = new FormControl('', Validators.required);
  reason = new FormControl('', Validators.required);
  reader = new FormControl('', Validators.required);
  book = new FormControl('', Validators.required);

  constructor(public serviceFine: FineService, fb: FormBuilder) {
    this.myForm = fb.group({
      id: this.id,
      size: this.size,
      reason: this.reason,
      reader: this.reader,
      book: this.book
    });
  };

  ngOnInit(): void {
    this.loadAll();

    this.currentUserId = localStorage.getItem('userId');
    this.currentUserClass = localStorage.getItem('userClass');
    this.isReader = this.currentUserClass == 'org.library.net.Reader'
    this.isLibrarian = this.currentUserClass == 'org.library.net.Librarian'
    this.isSupplier = this.currentUserClass == 'org.library.net.Supplier'
  }

  loadAll(): Promise<any> {
    const tempList = [];
    return this.serviceFine.getAll()
    .toPromise()
    .then((result) => {
      this.errorMessage = null;
      result.forEach(asset => {
        tempList.push(asset);
      });
      this.allAssets = tempList;
    })
    .catch((error) => {
      if (error === 'Server error') {
        this.errorMessage = 'Could not connect to REST server. Please check your configuration details';
      } else if (error === '404 - Not Found') {
        this.errorMessage = '404 - Could not find API route. Please check your available APIs.';
      } else {
        this.errorMessage = error;
      }
    });
  }

	/**
   * Event handler for changing the checked state of a checkbox (handles array enumeration values)
   * @param {String} name - the name of the asset field to update
   * @param {any} value - the enumeration value for which to toggle the checked state
   */
  changeArrayValue(name: string, value: any): void {
    const index = this[name].value.indexOf(value);
    if (index === -1) {
      this[name].value.push(value);
    } else {
      this[name].value.splice(index, 1);
    }
  }

	/**
	 * Checkbox helper, determining whether an enumeration value should be selected or not (for array enumeration values
   * only). This is used for checkboxes in the asset updateDialog.
   * @param {String} name - the name of the asset field to check
   * @param {any} value - the enumeration value to check for
   * @return {Boolean} whether the specified asset field contains the provided value
   */
  hasArrayValue(name: string, value: any): boolean {
    return this[name].value.indexOf(value) !== -1;
  }

  addAsset(form: any): Promise<any> {
    this.asset = {
      $class: 'org.library.net.Fine',
      'id': this.id.value,
      'size': this.size.value,
      'reason': this.reason.value,
      'reader': this.reader.value,
      'book': this.book.value
    };

    this.myForm.setValue({
      'id': null,
      'size': null,
      'reason': null,
      'reader': null,
      'book': null
    });

    return this.serviceFine.addAsset(this.asset)
    .toPromise()
    .then(() => {
      this.errorMessage = null;
      this.myForm.setValue({
        'id': null,
        'size': null,
        'reason': null,
        'reader': null,
        'book': null
      });
      this.loadAll();
    })
    .catch((error) => {
      if (error === 'Server error') {
          this.errorMessage = 'Could not connect to REST server. Please check your configuration details';
      } else {
          this.errorMessage = error;
      }
    });
  }


  updateAsset(form: any): Promise<any> {
    this.asset = {
      $class: 'org.library.net.Fine',
      'size': this.size.value,
      'reason': this.reason.value,
      'reader': this.reader.value,
      'book': this.book.value
    };

    return this.serviceFine.updateAsset(form.get('id').value, this.asset)
    .toPromise()
    .then(() => {
      this.errorMessage = null;
      this.loadAll();
    })
    .catch((error) => {
      if (error === 'Server error') {
        this.errorMessage = 'Could not connect to REST server. Please check your configuration details';
      } else if (error === '404 - Not Found') {
        this.errorMessage = '404 - Could not find API route. Please check your available APIs.';
      } else {
        this.errorMessage = error;
      }
    });
  }


  deleteAsset(): Promise<any> {

    return this.serviceFine.deleteAsset(this.currentId)
    .toPromise()
    .then(() => {
      this.errorMessage = null;
      this.loadAll();
    })
    .catch((error) => {
      if (error === 'Server error') {
        this.errorMessage = 'Could not connect to REST server. Please check your configuration details';
      } else if (error === '404 - Not Found') {
        this.errorMessage = '404 - Could not find API route. Please check your available APIs.';
      } else {
        this.errorMessage = error;
      }
    });
  }

  setId(id: any): void {
    this.currentId = id;
  }

  getForm(id: any): Promise<any> {

    return this.serviceFine.getAsset(id)
    .toPromise()
    .then((result) => {
      this.errorMessage = null;
      const formObject = {
        'id': null,
        'size': null,
        'reason': null,
        'reader': null,
        'book': null
      };

      if (result.id) {
        formObject.id = result.id;
      } else {
        formObject.id = null;
      }

      if (result.size) {
        formObject.size = result.size;
      } else {
        formObject.size = null;
      }

      if (result.reason) {
        formObject.reason = result.reason;
      } else {
        formObject.reason = null;
      }

      if (result.reader) {
        formObject.reader = result.reader;
      } else {
        formObject.reader = null;
      }

      if (result.book) {
        formObject.book = result.book;
      } else {
        formObject.book = null;
      }

      this.myForm.setValue(formObject);

    })
    .catch((error) => {
      if (error === 'Server error') {
        this.errorMessage = 'Could not connect to REST server. Please check your configuration details';
      } else if (error === '404 - Not Found') {
        this.errorMessage = '404 - Could not find API route. Please check your available APIs.';
      } else {
        this.errorMessage = error;
      }
    });
  }

  resetForm(): void {
    this.myForm.setValue({
      'id': null,
      'size': null,
      'reason': null,
      'reader': null,
      'book': null
      });
  }

}
