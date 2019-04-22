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

import { AngularTestPage } from './app.po';
import { ExpectedConditions, browser, element, by } from 'protractor';
import {} from 'jasmine';


describe('Starting tests for library-ui-app', function() {
  let page: AngularTestPage;

  beforeEach(() => {
    page = new AngularTestPage();
  });

  it('website title should be library-ui-app', () => {
    page.navigateTo('/');
    return browser.getTitle().then((result)=>{
      expect(result).toBe('library-ui-app');
    })
  });

  it('network-name should be library@0.1.2',() => {
    element(by.css('.network-name')).getWebElement()
    .then((webElement) => {
      return webElement.getText();
    })
    .then((txt) => {
      expect(txt).toBe('library@0.1.2.bna');
    });
  });

  it('navbar-brand should be library-ui-app',() => {
    element(by.css('.navbar-brand')).getWebElement()
    .then((webElement) => {
      return webElement.getText();
    })
    .then((txt) => {
      expect(txt).toBe('library-ui-app');
    });
  });

  
    it('Book component should be loadable',() => {
      page.navigateTo('/Book');
      browser.findElement(by.id('assetName'))
      .then((assetName) => {
        return assetName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('Book');
      });
    });

    it('Book table should have 11 columns',() => {
      page.navigateTo('/Book');
      element.all(by.css('.thead-cols th')).then(function(arr) {
        expect(arr.length).toEqual(11); // Addition of 1 for 'Action' column
      });
    });
  
    it('Fine component should be loadable',() => {
      page.navigateTo('/Fine');
      browser.findElement(by.id('assetName'))
      .then((assetName) => {
        return assetName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('Fine');
      });
    });

    it('Fine table should have 6 columns',() => {
      page.navigateTo('/Fine');
      element.all(by.css('.thead-cols th')).then(function(arr) {
        expect(arr.length).toEqual(6); // Addition of 1 for 'Action' column
      });
    });
  
    it('SupplyOrder component should be loadable',() => {
      page.navigateTo('/SupplyOrder');
      browser.findElement(by.id('assetName'))
      .then((assetName) => {
        return assetName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('SupplyOrder');
      });
    });

    it('SupplyOrder table should have 3 columns',() => {
      page.navigateTo('/SupplyOrder');
      element.all(by.css('.thead-cols th')).then(function(arr) {
        expect(arr.length).toEqual(3); // Addition of 1 for 'Action' column
      });
    });
  

  
    it('Admin component should be loadable',() => {
      page.navigateTo('/Admin');
      browser.findElement(by.id('participantName'))
      .then((participantName) => {
        return participantName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('Admin');
      });
    });

    it('Admin table should have 6 columns',() => {
      page.navigateTo('/Admin');
      element.all(by.css('.thead-cols th')).then(function(arr) {
        expect(arr.length).toEqual(6); // Addition of 1 for 'Action' column
      });
    });
  
    it('Reader component should be loadable',() => {
      page.navigateTo('/Reader');
      browser.findElement(by.id('participantName'))
      .then((participantName) => {
        return participantName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('Reader');
      });
    });

    it('Reader table should have 6 columns',() => {
      page.navigateTo('/Reader');
      element.all(by.css('.thead-cols th')).then(function(arr) {
        expect(arr.length).toEqual(6); // Addition of 1 for 'Action' column
      });
    });
  
    it('Librarian component should be loadable',() => {
      page.navigateTo('/Librarian');
      browser.findElement(by.id('participantName'))
      .then((participantName) => {
        return participantName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('Librarian');
      });
    });

    it('Librarian table should have 4 columns',() => {
      page.navigateTo('/Librarian');
      element.all(by.css('.thead-cols th')).then(function(arr) {
        expect(arr.length).toEqual(4); // Addition of 1 for 'Action' column
      });
    });
  
    it('Supplier component should be loadable',() => {
      page.navigateTo('/Supplier');
      browser.findElement(by.id('participantName'))
      .then((participantName) => {
        return participantName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('Supplier');
      });
    });

    it('Supplier table should have 6 columns',() => {
      page.navigateTo('/Supplier');
      element.all(by.css('.thead-cols th')).then(function(arr) {
        expect(arr.length).toEqual(6); // Addition of 1 for 'Action' column
      });
    });
  

  
    it('BookOrder component should be loadable',() => {
      page.navigateTo('/BookOrder');
      browser.findElement(by.id('transactionName'))
      .then((transactionName) => {
        return transactionName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('BookOrder');
      });
    });
  
    it('BookGiving component should be loadable',() => {
      page.navigateTo('/BookGiving');
      browser.findElement(by.id('transactionName'))
      .then((transactionName) => {
        return transactionName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('BookGiving');
      });
    });
  
    it('BookReturning component should be loadable',() => {
      page.navigateTo('/BookReturning');
      browser.findElement(by.id('transactionName'))
      .then((transactionName) => {
        return transactionName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('BookReturning');
      });
    });
  
    it('BooksSupply component should be loadable',() => {
      page.navigateTo('/BooksSupply');
      browser.findElement(by.id('transactionName'))
      .then((transactionName) => {
        return transactionName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('BooksSupply');
      });
    });
  
    it('FinePayment component should be loadable',() => {
      page.navigateTo('/FinePayment');
      browser.findElement(by.id('transactionName'))
      .then((transactionName) => {
        return transactionName.getText();
      })
      .then((txt) => {
        expect(txt).toBe('FinePayment');
      });
    });
  

});