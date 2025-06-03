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
 * @fileoverview This component provides a sidebar navigation mechanism for the application.
 * It leverages Angular Material's MatSidenav to offer a collapsible side panel,
 * typically used for navigation links or supplementary content.
 */

import { Component, ViewChild } from '@angular/core';
import { MatDrawer, MatSidenavModule } from '@angular/material/sidenav';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-sidebar',
  imports: [MatSidenavModule, MatButtonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css',
})
export class SidebarComponent {
  @ViewChild('sidenav') sidenav!: MatDrawer;

  /**
   * Toggles the open or closed state of the Material sidebar (MatDrawer).
   * This method is typically invoked by a button or another UI element to
   * show or hide the sidebar.
   * @returns {void}
   */
  toggle(): void {
    this.sidenav.toggle();
  }
}
