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

import { Component, Input, AfterViewInit, SimpleChanges } from '@angular/core';
import { MatTabChangeEvent, MatTabsModule } from '@angular/material/tabs';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import {
  ReactiveFormsModule,
  FormsModule,
  FormControl,
  FormRecord,
} from '@angular/forms';
import { Scene } from '../../models/scene-models';
import { Story } from '../../models/story-models';

@Component({
  selector: 'app-stories',
  imports: [
    MatTabsModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatDividerModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  templateUrl: './stories.component.html',
  styleUrl: './stories.component.css',
})
export class StoriesComponent {
  @Input() stories: Story[] = [];
  storiesForm = new FormRecord({});
  scenesFormControls: string[] = [];
  selectedTabIndex: number = 0;

  /**
   * Lifecycle hook that is called after Angular has fully initialized a component's view.
   * @returns {void}
   */
  ngAfterViewInit(): void {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['stories']) {
      console.log('myInput changed:', changes['stories'].currentValue);
      this.initScenesFormControls();
    }
  }

  onTabChanged(event: MatTabChangeEvent) {
    this.selectedTabIndex = event.index;
    this.updateScenesFormControls();
  }

  initScenesFormControls() {
    this.stories.forEach((story: Story, index: number) => {
      story.scenes.forEach((scene: Scene) => {
        const controlId = `${story.id}@${scene.id}`;
        this.storiesForm.addControl(
          controlId,
          new FormControl(scene.description)
        );
      });
    });
    this.updateScenesFormControls();
  }

  updateScenesFormControls() {
    const story = this.stories[this.selectedTabIndex];
    this.scenesFormControls = this.getStoriesControlNames().filter(
      (control: string) => {
        const storyId = control.split('@')[0];
        return storyId === story.id;
      }
    );
  }

  removeStoryFormControlbyId(id: string) {
    this.storiesForm.removeControl(id);
  }

  getStoriesControlNames(): string[] {
    return Object.keys(this.storiesForm.controls);
  }
}
