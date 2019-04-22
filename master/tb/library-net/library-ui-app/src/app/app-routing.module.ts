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

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home/home.component';
import { LoginComponent } from './Login/Login.component';

import { BookComponent } from './Book/Book.component';
import { FineComponent } from './Fine/Fine.component';
import { SupplyOrderComponent } from './SupplyOrder/SupplyOrder.component';

import { AdminComponent } from './Admin/Admin.component';
import { ReaderComponent } from './Reader/Reader.component';
import { LibrarianComponent } from './Librarian/Librarian.component';
import { SupplierComponent } from './Supplier/Supplier.component';

import { BookOrderComponent } from './BookOrder/BookOrder.component';
import { BookGivingComponent } from './BookGiving/BookGiving.component';
import { BookReturningComponent } from './BookReturning/BookReturning.component';
import { BooksSupplyComponent } from './BooksSupply/BooksSupply.component';
import { FinePaymentComponent } from './FinePayment/FinePayment.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'Book', component: BookComponent },
  { path: 'Fine', component: FineComponent },
  { path: 'SupplyOrder', component: SupplyOrderComponent },
  { path: 'Admin', component: AdminComponent },
  { path: 'Reader', component: ReaderComponent },
  { path: 'Librarian', component: LibrarianComponent },
  { path: 'Supplier', component: SupplierComponent },
  { path: 'BookOrder', component: BookOrderComponent },
  { path: 'BookGiving', component: BookGivingComponent },
  { path: 'BookReturning', component: BookReturningComponent },
  { path: 'BooksSupply', component: BooksSupplyComponent },
  { path: 'FinePayment', component: FinePaymentComponent },
  { path: 'Login', component: LoginComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
 imports: [RouterModule.forRoot(routes)],
 exports: [RouterModule],
 providers: []
})
export class AppRoutingModule { }
