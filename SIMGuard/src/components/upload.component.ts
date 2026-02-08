import { Component, inject, output, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SimGuardService } from '../services/simguard.service';
import { FileUploadResponse } from '../types';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="max-w-4xl mx-auto px-4 py-12">
      <div class="text-center mb-10">
        <h2 class="text-3xl font-bold text-white mb-2">Upload Log Files</h2>
        <p class="text-slate-400">Supported formats: .csv, .xlsx (Max 16MB)</p>
      </div>

      <!-- Drag & Drop Zone -->
      <div 
        class="relative group border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-300 cursor-pointer"
        [class]="isDragging() ? 'border-teal-500 bg-teal-500/10' : 'border-slate-700 bg-slate-900/50 hover:border-teal-500/50 hover:bg-slate-800/50'"
        (dragover)="onDragOver($event)"
        (dragleave)="onDragLeave($event)"
        (drop)="onDrop($event)"
        (click)="fileInput.click()">
        
        <input 
          #fileInput 
          type="file" 
          class="hidden" 
          accept=".csv,.xlsx,.xls"
          (change)="onFileSelected($event)">

        <div class="flex flex-col items-center gap-4">
          <div class="w-20 h-20 rounded-2xl bg-slate-800 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
            @if (isUploading()) {
              <i class="fas fa-circle-notch fa-spin text-teal-400 text-3xl"></i>
            } @else {
              <i class="fas fa-cloud-upload-alt text-teal-400 text-4xl"></i>
            }
          </div>
          
          <div class="space-y-2">
            <h3 class="text-xl font-semibold text-white">
              {{ isUploading() ? 'Uploading...' : 'Click or Drag file here' }}
            </h3>
            <p class="text-sm text-slate-400 max-w-sm mx-auto">
              Upload telecom logs containing Timestamp, User ID, SIM ID, Device ID, and Location.
            </p>
          </div>
        </div>
      </div>

      <!-- File Info & Action -->
      @if (uploadResult()) {
        <div class="mt-8 bg-slate-900 border border-slate-700 rounded-xl p-6 flex flex-col sm:flex-row items-center justify-between gap-6 animate-fade-in">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-lg bg-teal-500/20 flex items-center justify-center text-teal-400">
              <i class="fas fa-file-csv text-xl"></i>
            </div>
            <div>
              <h4 class="font-medium text-white">{{ uploadResult()?.filename }}</h4>
              <div class="flex items-center gap-3 text-xs text-slate-400 mt-1">
                <span><i class="fas fa-table mr-1"></i> {{ uploadResult()?.records_count }} Records</span>
                <span><i class="fas fa-clock mr-1"></i> {{ uploadResult()?.date_range?.start }}</span>
              </div>
            </div>
          </div>
          
          <button 
            (click)="triggerAnalysis()"
            [disabled]="isAnalyzing()"
            class="px-6 py-3 bg-teal-500 hover:bg-teal-400 text-slate-900 font-bold rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
            @if (isAnalyzing()) {
              <i class="fas fa-cog fa-spin"></i> Analyzing...
            } @else {
              <i class="fas fa-microchip"></i> Analyze Data
            }
          </button>
        </div>
      }

      @if (error()) {
        <div class="mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center gap-3 text-red-400">
          <i class="fas fa-exclamation-circle"></i>
          <span>{{ error() }}</span>
        </div>
      }
    </div>
  `,
  styles: [`
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .animate-fade-in { animation: fadeIn 0.4s ease-out; }
  `]
})
export class UploadComponent {
  service = inject(SimGuardService);
  analysisComplete = output<void>();

  isDragging = signal(false);
  isUploading = signal(false);
  isAnalyzing = signal(false);
  uploadResult = signal<FileUploadResponse | null>(null);
  error = signal<string | null>(null);

  onDragOver(e: DragEvent) {
    e.preventDefault();
    this.isDragging.set(true);
  }

  onDragLeave(e: DragEvent) {
    e.preventDefault();
    this.isDragging.set(false);
  }

  onDrop(e: DragEvent) {
    e.preventDefault();
    this.isDragging.set(false);
    if (e.dataTransfer?.files.length) {
      this.handleFile(e.dataTransfer.files[0]);
    }
  }

  onFileSelected(e: Event) {
    const input = e.target as HTMLInputElement;
    if (input.files?.length) {
      this.handleFile(input.files[0]);
    }
  }

  handleFile(file: File) {
    this.isUploading.set(true);
    this.error.set(null);
    this.uploadResult.set(null);

    this.service.uploadFile(file).subscribe({
      next: (res) => {
        this.uploadResult.set(res);
        this.service.uploadedFile.set(res.filename);
        this.isUploading.set(false);
      },
      error: (err) => {
        this.error.set('Failed to upload file. Ensure backend is running or check console.');
        this.isUploading.set(false);
      }
    });
  }

  triggerAnalysis() {
    this.isAnalyzing.set(true);
    this.service.analyzeData().subscribe({
      next: (res) => {
        // Fetch full results
        this.service.getResults().subscribe({
          next: (results) => {
            this.service.analysisData.set(results);
            this.isAnalyzing.set(false);
            this.analysisComplete.emit();
          },
          error: (err) => {
             this.error.set('Analysis completed but failed to fetch detailed results.');
             this.isAnalyzing.set(false);
          }
        })
      },
      error: (err) => {
        this.error.set('Analysis failed.');
        this.isAnalyzing.set(false);
      }
    });
  }
}
