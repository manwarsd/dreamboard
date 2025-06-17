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
 * @fileoverview This component facilitates brainstorming and generating video scenes based on user input.
 * It allows users to define a core idea and brand guidelines, specify the number of scenes,
 * generate scenes using a text generation service, and then select and export these scenes
 * for further video production. It includes a table with pagination and selection for managing scenes.
 */

import { Component, ViewChild, AfterViewInit, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { SelectionModel } from '@angular/cdk/collections';
import {
  Scene,
  ScenesGenerationRequest,
  VideoScene,
  SceneItem,
  ExportScenes,
} from '../../models/scene-models';
import { SelectItem } from '../../models/settings-models';
import { getNewVideoScene, getVideoFormats } from '../../video-utils';
import { ComponentsCommunicationService } from '../../services/components-communication.service';
import { openSnackBar } from '../../utils';
import { TextGenerationService } from '../../services/text-generation.service';
import { FileUploaderComponent } from '../file-uploader/file-uploader.component';
import { StoriesComponent } from '../stories/stories.component';
import {
  Story,
  StoryItem,
  StoriesGenerationRequest,
} from '../../models/story-models';

@Component({
  selector: 'app-brainstorm',
  imports: [
    MatButtonModule,
    MatInputModule,
    MatSelectModule,
    MatCheckboxModule,
    MatIconModule,
    MatPaginatorModule,
    MatTableModule,
    ReactiveFormsModule,
    FileUploaderComponent,
    StoriesComponent,
  ],
  templateUrl: './brainstorm.component.html',
  styleUrl: './brainstorm.component.css',
})
export class BrainstormComponent implements AfterViewInit {
  stories: Story[] = [];

  displayedColumns: string[] = [
    'number',
    'description',
    'brandGuidelinesAlignment',
    'imagePrompt',
    'select',
  ];
  scenes: Scene[] = [];
  dataSource = new MatTableDataSource<Scene>(this.scenes);
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  private _snackBar = inject(MatSnackBar);
  videoFormats: SelectItem[] = getVideoFormats();

  scenesSettingsForm = new FormGroup({
    idea: new FormControl('', [Validators.required]),
    brandGuidelines: new FormControl('', []),
    numScenes: new FormControl(1, [Validators.required]),
    replaceGeneratedScenes: new FormControl(true, []),
    generateInitialImageForScenes: new FormControl(false, []),
  });

  constructor(
    private componentsCommunicationService: ComponentsCommunicationService,
    private textGenerationService: TextGenerationService
  ) {}

  /**
   * Checks whether the number of selected scenes matches the total number of rows in the table.
   * This is used to determine the state of the "select all" checkbox.
   * @returns {boolean} `true` if all rows are selected, `false` otherwise.
   */
  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }

  selection = new SelectionModel<Scene>(true, []);

  /**
   * Checks whether the number of selected scenes matches the total number of rows in the table.
   * This is used to determine the state of the "select all" checkbox.
   * @returns {boolean} `true` if all rows are selected, `false` otherwise.
   */
  isAllSelected(): boolean {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /**
   * Toggles the selection state of all rows in the table.
   * If all rows are currently selected, it clears the selection. Otherwise, it selects all rows.
   * @returns {void}
   */
  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.dataSource.data);
  }

  /**
   * Provides the accessibility label for the checkbox on a given row or the "select all" checkbox.
   * @param {Scene} [row] - The optional `Scene` object for which to generate the label.
   * @returns {string} The accessibility label for the checkbox.
   */
  checkboxLabel(row?: Scene): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${
      row.number + 1
    }`;
  }

  /**
   * Exports the currently selected scenes to the `SceneBuilderComponent` for further processing.
   * Validates that at least one scene is selected before proceeding.
   * Displays snackbar messages indicating the export status and whether initial images will be generated.
   * Updates the `ComponentsCommunicationService` to notify other components of the exported scenes and
   * to switch to the Scene Builder tab.
   * @returns {void}
   */
  exportScenes(): void {
    if (this.selection.selected.length == 0) {
      openSnackBar(
        this._snackBar,
        'No scenes have been selected. Please select at least 1 scene and try again.',
        20
      );
      return;
    }
    const generateImages = this.scenesSettingsForm.get(
      'generateInitialImageForScenes'
    )?.value!;

    if (generateImages) {
      openSnackBar(
        this._snackBar,
        'Exporting scenes and generating initial images... Please wait.'
      );
    } else {
      openSnackBar(this._snackBar, 'Exporting scenes... Please wait.');
    }

    // Export only selected scenes
    const videoScenes: VideoScene[] = this.selection.selected.map(
      (scene: Scene, index: number) => {
        const videoScene = getNewVideoScene(index);
        videoScene.description = scene.description;
        videoScene.imageGenerationSettings.prompt = scene.imagePrompt;
        return videoScene;
      }
    );
    const exportScenes: ExportScenes = {
      videoScenes: videoScenes,
      replaceExistingScenesOnExport: true,
      generateInitialImageForScenes: generateImages,
    };
    this.componentsCommunicationService.scenesExported(exportScenes);
    this.componentsCommunicationService.tabChanged(1);
  }

  generateStories(): void {
    openSnackBar(this._snackBar, 'Generating stories... Please wait.');

    const storiesGeneration = this.getStoriesGenerationParams();
    this.textGenerationService.generateStories(storiesGeneration).subscribe(
      (generatedStories: StoryItem[]) => {
        openSnackBar(
          this._snackBar,
          `${generatedStories.length} ${
            generatedStories.length > 0 ? 'stories' : 'story'
          } generated successfully!`,
          20
        );
        this.stories = generatedStories.map((genStory: StoryItem) => {
          const story: Story = {
            id: genStory.id,
            title: genStory.title,
            description: genStory.description,
            abcdAdherence: genStory.abcd_adherence,
            scenes: [],
          };
          story.scenes = genStory.scenes.map((genScene: SceneItem) => {
            const scene: Scene = {
              id: genScene.id,
              number: genScene.number,
              description: genScene.description,
              imagePrompt: genScene.image_prompt,
            };
            return scene;
          });
          return story;
        });
      },
      (error: any) => {
        let errorMessage;
        if (error.error.hasOwnProperty('detail')) {
          errorMessage = error.error.detail;
        } else {
          errorMessage = error.error.message;
        }
        console.error(errorMessage);
        openSnackBar(
          this._snackBar,
          `ERROR: ${errorMessage}. Please try again.`
        );
      }
    );
  }

  /**
   * Initiates the generation of new scenes based on the user's idea, brand guidelines,
   * and desired number of scenes.
   * Displays snackbar messages for the generation status.
   * Upon successful generation, it updates the `scenes` array, either replacing existing ones
   * or appending to them, and refreshes the table data source.
   * Handles and displays error messages from the API.
   * @returns {void}
   */
  generateScenes(): void {
    openSnackBar(this._snackBar, 'Generating scenes... Please wait.');

    const sceneGeneration = this.getScenesGenerationParams();
    this.textGenerationService.generateScenes(sceneGeneration).subscribe(
      (generatedScenes: SceneItem[]) => {
        openSnackBar(
          this._snackBar,
          `${generatedScenes.length} ${
            generatedScenes.length > 0 ? 'scenes' : 'scene'
          } generated successfully!`,
          20
        );
        const replaceGeneratedScenes = this.scenesSettingsForm.get(
          'replaceGeneratedScenes'
        )?.value!;
        const genScenes: Scene[] = generatedScenes.map(
          (genScene: SceneItem) => {
            return {
              id: '', // TODO (ae) change this
              number: genScene.number,
              description: genScene.description,
              imagePrompt: genScene.image_prompt,
            };
          }
        );
        if (replaceGeneratedScenes) {
          this.scenes = genScenes;
          // Also clear selection
          this.selection.clear();
        } else {
          this.scenes.push.apply(this.scenes, genScenes);
        }
        this.dataSource.data = this.scenes;
      },
      (error: any) => {
        let errorMessage;
        if (error.error.hasOwnProperty('detail')) {
          errorMessage = error.error.detail;
        } else {
          errorMessage = error.error.message;
        }
        console.error(errorMessage);
        openSnackBar(
          this._snackBar,
          `ERROR: ${errorMessage}. Please try again.`
        );
      }
    );
  }

  getStoriesGenerationParams() {
    const storiesGenerationRequest: StoriesGenerationRequest = {
      creative_brief_idea: '',
      target_audience: '',
      brand_guidelines: '',
      video_format: '',
      num_scenes: 1
    };

    return storiesGenerationRequest;
  }

  /**
   * Constructs a `ScenesGenerationRequest` object from the current values in the `scenesSettingsForm`.
   * This object is used to send to the text generation API to request new scenes.
   * @returns {ScenesGenerationRequest} The constructed scenes generation request.
   */
  getScenesGenerationParams() {
    return {
      idea: this.scenesSettingsForm.get('idea')?.value,
      brand_guidelines: this.scenesSettingsForm.get('brandGuidelines')?.value,
      num_scenes: this.scenesSettingsForm.get('numScenes')?.value,
    } as ScenesGenerationRequest;
  }

  /**
   * Determines whether the "Generate Scenes" button should be disabled.
   * The button is enabled only if the `scenesSettingsForm` is valid (e.g., idea and number of scenes are filled).
   * @returns {boolean} `true` if the button should be disabled, `false` otherwise.
   */
  disableGenerateScenesButton() {
    return !this.scenesSettingsForm.valid;
  }
}
