/***************************************************************************
 *
 *  Copyright 2025 Google Inc.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Note that these code samples being shared are not official Google
 *  products and are not formally supported.
 *
 ***************************************************************************/

/**
 * @fileoverview This component defines a custom Angular Material snackbar.
 * It provides a basic structure for displaying messages to the user,
 * typically with an action button to dismiss the snackbar.
 */

import { Component, inject } from '@angular/core';
import { MatSnackBarRef } from '@angular/material/snack-bar';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-snackbar',
  imports: [MatButtonModule],
  templateUrl: './snackbar.component.html',
  styleUrl: './snackbar.component.css',
})
export class SnackbarComponent {
  snackBarRef = inject(MatSnackBarRef);
}
