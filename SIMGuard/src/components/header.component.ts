
import { Component, output, input } from '@angular/core';
import { ViewState } from '../types';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  template: `
    <header class="bg-slate-900 border-b border-slate-800 sticky top-0 z-50 backdrop-blur-md bg-opacity-90">
      <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center gap-3 cursor-pointer" (click)="navigate.emit('home')">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-400 to-teal-600 flex items-center justify-center shadow-lg shadow-teal-500/20">
            <i class="fas fa-shield-alt text-white text-sm"></i>
          </div>
          <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            SIMGuard
          </span>
        </div>

        <!-- Navigation -->
        <div class="hidden md:flex items-center gap-1">
          <button 
            (click)="navigate.emit('home')"
            [class]="isActive('home')"
            class="nav-btn">
            Home
          </button>
          
          <div class="h-4 w-px bg-slate-700 mx-2"></div>

          <button 
            (click)="navigate.emit('ml-manual')"
            [class]="isActive('ml-manual')"
            class="nav-btn">
            <i class="fas fa-sliders-h mr-1.5"></i> Manual Check
          </button>

          <button 
            (click)="navigate.emit('upload')"
            [class]="isActive('upload')"
            class="nav-btn">
            <i class="fas fa-layer-group mr-1.5"></i> Batch Analysis (ML)
          </button>
        </div>

        <!-- Mobile Menu (Simple) -->
        <div class="md:hidden text-slate-400">
          <i class="fas fa-bars text-xl"></i>
        </div>
      </nav>
    </header>
  `,
  styles: [`
    .nav-btn {
      @apply px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 text-slate-400 hover:text-white hover:bg-slate-800;
    }
    .active-nav {
      @apply text-teal-400 bg-slate-800;
    }
  `]
})
export class HeaderComponent {
  currentView = input.required<ViewState>();
  navigate = output<ViewState>();

  isActive(view: ViewState): string {
    return this.currentView() === view ? 'active-nav nav-btn' : 'nav-btn';
  }
}
