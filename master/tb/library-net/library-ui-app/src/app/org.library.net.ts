import {Asset} from './org.hyperledger.composer.system';
import {Participant} from './org.hyperledger.composer.system';
import {Transaction} from './org.hyperledger.composer.system';
import {Event} from './org.hyperledger.composer.system';
// export namespace org.library.net{
   export class Book extends Asset {
      id: string;
      name: string;
      author: string;
      description: string;
      supplied: boolean;
      supplier: Supplier;
      ordered: boolean;
      onHands: boolean;
      givingDate: Date;
      currentReader: Reader;
   }
   export class Fine extends Asset {
      id: string;
      size: number;
      reason: string;
      reader: Reader;
      book: Book;
   }
   export class SupplyOrder extends Asset {
      id: string;
      book: Book;
   }
   export class Admin extends Participant {
      id: string;
      firstName: string;
      lastName: string;
      phoneNumber: string;
      email: string;
   }
   export class Reader extends Participant {
      id: string;
      firstName: string;
      lastName: string;
      phoneNumber: string;
      email: string;
   }
   export class Librarian extends Participant {
      id: string;
      firstName: string;
      lastName: string;
   }
   export class Supplier extends Participant {
      id: string;
      firstName: string;
      lastName: string;
      phoneNumber: string;
      email: string;
   }
   export class BookOrder extends Transaction {
      book: Book;
      reader: Reader;
   }
   export class BookGiving extends Transaction {
      book: Book;
      reader: Reader;
      librarian: Librarian;
   }
   export class BookReturning extends Transaction {
      book: Book;
      reader: Reader;
      librarian: Librarian;
   }
   export class BooksSupply extends Transaction {
      supplier: Supplier;
      order: SupplyOrder;
   }
   export class FinePayment extends Transaction {
      fine: Fine;
      reader: Reader;
   }
// }
