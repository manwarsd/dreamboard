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

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';
import { ScenesGenerationRequest } from '../models/scene-models';
import { StoriesGenerationRequest } from '../models/story-models';
import { environment } from '../../environments/environment.development';
import { Title } from '@angular/platform-browser';

@Injectable({
  providedIn: 'root',
})
export class TextGenerationService {
  BASE_URL = environment.textGenerationApiURL;

  constructor(private http: HttpClient) {}

  generateStories(storiesGeneration: StoriesGenerationRequest): any {
    /*return this.http.post<any[]>(
      `${this.BASE_URL}/generate_stories`,
      storiesGeneration
    );*/

    const response = [
      {
        id: '123',
        title: 'A cat in the moon',
        description: 'Story 1 description',
        abcd_adherence: 'Attract is good',
        scenes: [
          {
            id: '87967',
            number: '1',
            description: 'Scene 1 description',
            imagePrompt: 'prompt 1',
          },
          {
            id: '45645',
            number: '2',
            description: 'Scene 2 description',
            imagePrompt: 'prompt 2',
          },
        ],
      },
      {
        id: '456',
        title: 'A dog in the sun',
        description: 'Story 2 description',
        abcd_adherence: 'Attract is good',
        scenes: [
          {
            id: '34645',
            number: '1',
            description: 'Scene 1 description',
            imagePrompt: 'prompt 1',
          },
          {
            id: '45645',
            number: '2',
            description: 'Scene 2 description',
            imagePrompt: 'prompt 2',
          },
        ],
      },
      {
        id: '789',
        title: 'Cats and dogs',
        description: 'Story 3 description',
        abcd_adherence: 'Attract is good',
        scenes: [
          {
            id: '45645',
            number: '1',
            description: 'Scene 1 description',
            imagePrompt: 'prompt 1',
          },
          {
            id: '45645',
            number: '2',
            description: 'Scene 2 description',
            imagePrompt: 'prompt 2',
          },
        ],
      },
    ];

    return of(response);
  }

  generateScenes(scenesGeneration: ScenesGenerationRequest): any {
    return this.http.post<any[]>(
      `${this.BASE_URL}/brainstorm_scenes`,
      scenesGeneration
    );
  }

  rewriteImagePrompt(
    prompt: string,
    scene_description: string,
    withSceneDescription: boolean
  ): any {
    // Change Endpoints because prompts are different
    if (withSceneDescription) {
      return this.http.post<any>(
        `${this.BASE_URL}/enhance_image_prompt_with_scene`,
        { prompt: prompt, scene: scene_description }
      );
    } else {
      return this.http.post<any>(`${this.BASE_URL}/enhance_image_prompt`, {
        prompt: prompt,
        scene: scene_description,
      });
    }
  }

  rewriteVideoPrompt(
    prompt: string,
    scene_description: string,
    withSceneDescription: boolean
  ): any {
    // Change Endpoints because prompts are different
    if (withSceneDescription) {
      return this.http.post<any>(
        `${this.BASE_URL}/enhance_video_prompt_with_scene`,
        { prompt: prompt, scene: scene_description }
      );
    } else {
      return this.http.post<any>(`${this.BASE_URL}/enhance_video_prompt`, {
        prompt: prompt,
        scene: scene_description,
      });
    }
  }

  rewriteBrainstormPrompt(idea: string): any {
    return this.http.post<any>(`${this.BASE_URL}/rewrite_brainstorm_prompt`, {
      idea: idea,
    });
  }
}
