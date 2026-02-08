
import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './components/header.component';
import { HeroComponent } from './components/hero.component';
import { UploadComponent } from './components/upload.component';
import { DashboardComponent } from './components/dashboard.component';
import { MlManualComponent } from './components/ml-manual.component';
import { ViewState } from './types';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule, 
    HeaderComponent, 
    HeroComponent, 
    UploadComponent, 
    DashboardComponent,
    MlManualComponent
  ],
  template: `
    <app-header [currentView]="view()" (navigate)="setView($event)"></app-header>
    <main class="min-h-[calc(100vh-64px)] bg-slate-950 text-slate-200">
      @switch (view()) {
        @case ('home') { <app-hero (start)="setView('ml-manual')" class="block h-[calc(100vh-64px)]" /> }
        @case ('upload') { <app-upload (analysisComplete)="setView('dashboard')" /> }
        @case ('dashboard') { <app-dashboard /> }
        @case ('ml-manual') { <app-ml-manual /> }
      }
    </main>
  `
})
export class AppComponent {
  view = signal<ViewState>('home');

  setView(newView: ViewState) {
    this.view.set(newView);
  }
}