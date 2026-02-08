import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SimGuardService } from '../services/simguard.service';
import { TrainResponse } from '../types';

@Component({
  selector: 'app-sl-training',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="max-w-7xl mx-auto px-4 py-8">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-white flex items-center gap-3">
            <i class="fas fa-brain text-teal-400"></i> Sri Lankan ML Dashboard
          </h1>
          <p class="text-slate-400 mt-1">Train custom models on local telecom datasets (Dialog, Mobitel, etc.)</p>
        </div>
        <div class="px-4 py-1 bg-teal-900/30 border border-teal-500/30 rounded-full text-teal-400 text-sm font-semibold">
          🇱🇰 Sri Lanka Region
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        <!-- Left: Upload & Config -->
        <div class="space-y-6">
          <!-- Upload Card -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 class="text-xl font-semibold text-white mb-4"><i class="fas fa-upload mr-2"></i> Training Dataset</h2>
            
            <div class="border-2 border-dashed border-slate-700 rounded-lg p-8 text-center bg-slate-800/30 hover:bg-slate-800/50 transition-colors cursor-pointer"
                 (click)="fileInput.click()">
              <input #fileInput type="file" class="hidden" (change)="onFileSelected($event)" accept=".xlsx,.xls,.csv">
              <i class="fas fa-file-excel text-4xl text-teal-500 mb-3"></i>
              <p class="text-slate-300 font-medium">{{ selectedFileName() || 'Click to Upload Excel/CSV' }}</p>
            </div>
            
            @if (selectedFileName()) {
              <button (click)="uploadFile()" [disabled]="uploading()" class="w-full mt-4 bg-slate-700 hover:bg-slate-600 text-white py-2 rounded transition-colors text-sm">
                {{ uploading() ? 'Uploading...' : 'Confirm Dataset' }}
              </button>
            }
          </div>

          <!-- Training Config -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 class="text-xl font-semibold text-white mb-4"><i class="fas fa-cogs mr-2"></i> Model Configuration</h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm text-slate-400 mb-1">Model Architecture</label>
                <select [(ngModel)]="modelType" class="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white">
                  <option value="xgboost">XGBoost Classifier (Recommended)</option>
                  <option value="random_forest">Random Forest</option>
                  <option value="logistic">Logistic Regression</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm text-slate-400 mb-1">Test Set Size (%)</label>
                <input type="number" [(ngModel)]="testSize" class="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white" min="10" max="50">
              </div>

              <button 
                (click)="train()" 
                [disabled]="training() || !isFileUploaded()"
                class="w-full bg-teal-600 hover:bg-teal-500 text-white font-bold py-3 rounded-lg flex justify-center items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
                @if (training()) { <i class="fas fa-sync fa-spin"></i> Training... }
                @else { <i class="fas fa-play"></i> Train Model }
              </button>
            </div>
          </div>
        </div>

        <!-- Right: Results -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col">
          <h2 class="text-xl font-semibold text-white mb-4"><i class="fas fa-chart-line mr-2"></i> Performance Metrics</h2>
          
          @if (!results()) {
            <div class="flex-1 flex flex-col items-center justify-center text-slate-500 min-h-[300px]">
              <i class="fas fa-microchip text-5xl mb-4 opacity-20"></i>
              <p>Train a model to view metrics</p>
            </div>
          } @else {
            <div class="space-y-6 animate-fade-in">
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-slate-800 p-4 rounded-lg text-center">
                  <p class="text-slate-400 text-xs uppercase">Accuracy</p>
                  <p class="text-2xl font-bold text-teal-400">{{ results()!.metrics.accuracy * 100 | number:'1.1-1' }}%</p>
                </div>
                <div class="bg-slate-800 p-4 rounded-lg text-center">
                  <p class="text-slate-400 text-xs uppercase">Precision</p>
                  <p class="text-2xl font-bold text-blue-400">{{ results()!.metrics.precision * 100 | number:'1.1-1' }}%</p>
                </div>
                <div class="bg-slate-800 p-4 rounded-lg text-center">
                  <p class="text-slate-400 text-xs uppercase">Recall</p>
                  <p class="text-2xl font-bold text-purple-400">{{ results()!.metrics.recall * 100 | number:'1.1-1' }}%</p>
                </div>
                <div class="bg-slate-800 p-4 rounded-lg text-center">
                  <p class="text-slate-400 text-xs uppercase">F1 Score</p>
                  <p class="text-2xl font-bold text-amber-400">{{ results()!.metrics.f1_score * 100 | number:'1.1-1' }}%</p>
                </div>
              </div>

              <div class="border-t border-slate-800 pt-4">
                <h3 class="text-white font-medium mb-3">Confusion Matrix</h3>
                <div class="grid grid-cols-2 gap-1 text-center text-sm font-mono">
                  <div class="bg-slate-950 p-2 text-slate-400">True Neg</div>
                  <div class="bg-slate-950 p-2 text-slate-400">False Pos</div>
                  <div class="bg-teal-900/30 p-4 rounded text-white">{{ results()!.confusion_matrix[0][0] }}</div>
                  <div class="bg-red-900/30 p-4 rounded text-white">{{ results()!.confusion_matrix[0][1] }}</div>
                  
                  <div class="bg-slate-950 p-2 text-slate-400">False Neg</div>
                  <div class="bg-slate-950 p-2 text-slate-400">True Pos</div>
                  <div class="bg-red-900/30 p-4 rounded text-white">{{ results()!.confusion_matrix[1][0] }}</div>
                  <div class="bg-teal-900/30 p-4 rounded text-white">{{ results()!.confusion_matrix[1][1] }}</div>
                </div>
              </div>
            </div>
          }
        </div>
      </div>
    </div>
  `,
  styles: [`
    .animate-fade-in { animation: fadeIn 0.5s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  `]
})
export class SlTrainingComponent {
  service = inject(SimGuardService);
  
  selectedFile = signal<File | null>(null);
  selectedFileName = signal<string>('');
  isFileUploaded = signal(false);
  uploading = signal(false);
  training = signal(false);
  
  modelType: any = 'xgboost';
  testSize = 20;
  
  results = signal<TrainResponse | null>(null);

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile.set(file);
      this.selectedFileName.set(file.name);
      this.isFileUploaded.set(false); // require re-upload if file changes
    }
  }

  uploadFile() {
    if (!this.selectedFile()) return;
    this.uploading.set(true);
    this.service.uploadTrainingFile(this.selectedFile()!).subscribe({
      next: () => {
        this.uploading.set(false);
        this.isFileUploaded.set(true);
      },
      error: () => this.uploading.set(false)
    });
  }

  train() {
    this.training.set(true);
    this.service.trainModel({
      model_type: this.modelType,
      test_size: this.testSize
    }).subscribe({
      next: (res) => {
        this.results.set(res);
        this.training.set(false);
      },
      error: () => this.training.set(false)
    });
  }
}