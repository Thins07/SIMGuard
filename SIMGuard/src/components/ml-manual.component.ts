
import { Component, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SimGuardService } from '../services/simguard.service';
import { PredictionResponse } from '../types';

@Component({
  selector: 'app-ml-manual',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="max-w-7xl mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Left Panel: Input Form -->
        <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div class="mb-6 pb-6 border-b border-slate-800">
            <h1 class="text-2xl font-bold text-white flex items-center gap-3">
              <i class="fas fa-search text-teal-400"></i> Manual Investigation
            </h1>
            <p class="text-slate-400 mt-2">Enter subscriber telemetry to detect anomalies. High-risk indicators are highlighted automatically.</p>
          </div>

          <form [formGroup]="form" (ngSubmit)="analyze()">
            <div class="space-y-6">
              
              <!-- Section 1: Core Behavioral Metrics -->
              <div>
                <h3 class="text-teal-400 font-medium mb-4 uppercase text-xs tracking-wider flex items-center gap-2">
                  <i class="fas fa-signal"></i> Behavioral Telemetry
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  
                  <!-- Time Since SIM Change -->
                  <div class="form-group relative">
                    <label class="block text-sm text-slate-300 mb-1 flex justify-between">
                      Time Since SIM Change (hrs)
                      @if (isSimChangeRisky()) { <span class="text-red-400 text-xs font-bold animate-pulse">HIGH RISK (&lt;48h)</span> }
                    </label>
                    <div class="relative">
                      <input type="number" formControlName="time_since_sim_change" 
                        [class.border-red-500]="isSimChangeRisky()"
                        [class.focus:ring-red-500]="isSimChangeRisky()"
                        class="w-full bg-slate-800 border border-slate-700 rounded-lg pl-3 pr-10 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none transition-all">
                      @if (isSimChangeRisky()) {
                        <i class="fas fa-exclamation-circle text-red-500 absolute right-3 top-3"></i>
                      }
                    </div>
                  </div>

                  <!-- Distance Change -->
                  <div class="form-group">
                    <label class="block text-sm text-slate-300 mb-1 flex justify-between">
                      Distance Change (km)
                      @if (isDistanceRisky()) { <span class="text-amber-400 text-xs font-bold">ABNORMAL (&gt;100km)</span> }
                    </label>
                    <div class="relative">
                      <input type="number" formControlName="distance_change" 
                        [class.border-amber-500]="isDistanceRisky()"
                        [class.focus:ring-amber-500]="isDistanceRisky()"
                        class="w-full bg-slate-800 border border-slate-700 rounded-lg pl-3 pr-10 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none transition-all">
                        @if (isDistanceRisky()) {
                          <i class="fas fa-exclamation-triangle text-amber-500 absolute right-3 top-3"></i>
                        }
                    </div>
                  </div>

                  <!-- Data Usage Change -->
                  <div class="form-group">
                    <label class="block text-sm text-slate-300 mb-1 flex justify-between">
                      Data Usage Change (%)
                      @if (isDataSpikeRisky()) { <span class="text-red-400 text-xs font-bold">USAGE SPIKE</span> }
                    </label>
                    <input type="number" formControlName="data_usage_change_percent" 
                      [class.border-red-500]="isDataSpikeRisky()"
                      class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none">
                  </div>

                  <!-- Data Usage Volume -->
                   <div class="form-group">
                    <label class="block text-sm text-slate-300 mb-1">Data Usage (24h) MB</label>
                    <input type="number" formControlName="data_usage_last_24h" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none">
                  </div>
                </div>
              </div>

              <!-- Section 2: Activity Counters -->
              <div>
                <h3 class="text-slate-500 font-medium mb-4 uppercase text-xs tracking-wider flex items-center gap-2">
                  <i class="fas fa-list-ol"></i> Activity Counters
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div class="form-group">
                    <label class="block text-sm text-slate-300 mb-1">Failed Logins (24h)</label>
                    <input type="number" formControlName="num_failed_logins_last_24h" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none">
                  </div>
                  <div class="form-group">
                    <label class="block text-sm text-slate-300 mb-1">Num Calls (24h)</label>
                    <input type="number" formControlName="num_calls_last_24h" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none">
                  </div>
                  <div class="form-group">
                    <label class="block text-sm text-slate-300 mb-1">Num SMS (24h)</label>
                    <input type="number" formControlName="num_sms_last_24h" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none">
                  </div>
                </div>
              </div>

              <!-- Section 3: Flags & Location -->
              <div class="bg-slate-800/30 p-4 rounded-xl border border-slate-700/50">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 class="text-slate-400 font-medium mb-3 text-xs uppercase">Status Flags</h3>
                    <div class="space-y-3">
                      <label class="flex items-center gap-3 cursor-pointer p-2 rounded hover:bg-slate-800 transition-colors">
                        <div class="relative">
                          <input type="checkbox" formControlName="is_roaming" class="peer sr-only">
                          <div class="w-10 h-6 bg-slate-700 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-teal-600"></div>
                        </div>
                        <span class="text-slate-200 text-sm">International Roaming</span>
                      </label>
                      <label class="flex items-center gap-3 cursor-pointer p-2 rounded hover:bg-slate-800 transition-colors">
                        <div class="relative">
                          <input type="checkbox" formControlName="sim_change_flag" class="peer sr-only">
                          <div class="w-10 h-6 bg-slate-700 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-red-500"></div>
                        </div>
                        <span class="text-slate-200 text-sm">Recent SIM Change Flag</span>
                      </label>
                    </div>
                  </div>
                  
                  <div>
                    <h3 class="text-slate-400 font-medium mb-3 text-xs uppercase">Location Context</h3>
                    <div class="space-y-3">
                      <div>
                        <input type="text" formControlName="current_city" placeholder="Current City" class="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:border-teal-500 outline-none">
                      </div>
                      <div>
                        <input type="text" formControlName="previous_city" placeholder="Previous City" class="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:border-teal-500 outline-none">
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="flex gap-4 pt-4 border-t border-slate-800">
                <button type="submit" [disabled]="isAnalyzing()" class="flex-1 bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-400 hover:to-teal-500 text-slate-900 font-bold py-3 px-6 rounded-lg transition-all shadow-lg shadow-teal-500/20 flex justify-center items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
                  @if (isAnalyzing()) { <i class="fas fa-circle-notch fa-spin"></i> Processing }
                  @else { <i class="fas fa-search-location"></i> Run Analysis }
                </button>
                <button type="button" (click)="resetForm()" class="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg border border-slate-700 transition-colors">
                  Reset
                </button>
              </div>

            </div>
          </form>
        </div>

        <!-- Right Panel: Results -->
        <div class="lg:col-span-1">
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 h-full flex flex-col items-center justify-center text-center min-h-[400px] sticky top-24">
            
            @if (!result() && !isAnalyzing()) {
              <div class="text-slate-500">
                <div class="w-20 h-20 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-6">
                  <i class="fas fa-fingerprint text-4xl opacity-50"></i>
                </div>
                <h2 class="text-xl font-semibold text-white mb-2">Ready to Analyze</h2>
                <p class="text-sm max-w-xs mx-auto">Fill in the telemetry data to run the detection model against the entered parameters.</p>
              </div>
            }

            @if (isAnalyzing()) {
              <div class="text-teal-400 animate-pulse">
                <i class="fas fa-brain text-6xl mb-4"></i>
                <p class="text-xl font-semibold">Analyzing Patterns...</p>
                <p class="text-xs text-slate-500 mt-2">Running XGBoost Inference</p>
              </div>
            }

            @if (result(); as res) {
              <div class="w-full animate-fade-in">
                <div class="w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 text-4xl shadow-2xl relative"
                  [class]="res.risk_level === 'HIGH' ? 'bg-red-500 text-white shadow-red-500/50' : (res.risk_level === 'MEDIUM' ? 'bg-amber-500 text-white shadow-amber-500/50' : 'bg-teal-500 text-white shadow-teal-500/50')">
                  <i [class]="res.risk_level === 'HIGH' ? 'fas fa-radiation' : (res.risk_level === 'MEDIUM' ? 'fas fa-exclamation-triangle' : 'fas fa-shield-alt')"></i>
                  
                  <!-- Ripple effect for High Risk -->
                  <div *ngIf="res.risk_level === 'HIGH'" class="absolute inset-0 rounded-full border-4 border-red-500 opacity-75 animate-ping"></div>
                </div>
                
                <h2 class="text-3xl font-bold mb-1" 
                  [class]="res.risk_level === 'HIGH' ? 'text-red-400' : (res.risk_level === 'MEDIUM' ? 'text-amber-400' : 'text-teal-400')">
                  {{ res.risk_level }} RISK
                </h2>
                <p class="text-xs font-mono text-slate-500 uppercase tracking-widest mb-6">Confidence: {{ (res.confidence * 100) | number:'1.0-1' }}%</p>
                
                <div class="bg-slate-950 rounded-lg p-4 border border-slate-800 text-left mb-6">
                  <p class="text-slate-300 text-sm leading-relaxed"><i class="fas fa-info-circle mr-2 text-slate-500"></i>{{ res.message }}</p>
                </div>

                <div class="space-y-3">
                   <div class="flex justify-between text-xs text-slate-400 uppercase">
                     <span>Threat Likelihood</span>
                     <span>{{ (res.confidence * 100) | number:'1.0-0' }}%</span>
                   </div>
                   <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div class="h-full transition-all duration-1000 ease-out"
                      [style.width.%]="res.confidence * 100"
                      [class]="res.risk_level === 'HIGH' ? 'bg-red-500' : (res.risk_level === 'MEDIUM' ? 'bg-amber-500' : 'bg-teal-500')">
                    </div>
                  </div>
                </div>
              </div>
            }
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .animate-fade-in { animation: fadeIn 0.5s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  `]
})
export class MlManualComponent {
  private fb: FormBuilder = inject(FormBuilder);
  service = inject(SimGuardService);
  
  isAnalyzing = signal(false);
  result = signal<PredictionResponse | null>(null);

  form: FormGroup = this.fb.group({
    distance_change: [0, Validators.required],
    time_since_sim_change: [100, Validators.required], // Default to safe value
    num_failed_logins_last_24h: [0, Validators.required],
    num_calls_last_24h: [0, Validators.required],
    num_sms_last_24h: [0, Validators.required],
    data_usage_last_24h: [0, Validators.required],
    data_usage_change_percent: [0, Validators.required],
    change_in_cell_tower_id: [0],
    is_roaming: [false],
    sim_change_flag: [false],
    device_change_flag: [false],
    current_city: ['Colombo', Validators.required],
    previous_city: ['Colombo', Validators.required]
  });

  // --- Real-time Logic ---
  
  isSimChangeRisky = computed(() => {
    const val = this.form.get('time_since_sim_change')?.value;
    // Highlight if sim change happened within last 48 hours
    return val !== null && val < 48;
  });

  isDistanceRisky = computed(() => {
    const val = this.form.get('distance_change')?.value;
    // Highlight if distance is large (>100km) implying impossible travel or anomaly
    return val !== null && val > 100;
  });

  isDataSpikeRisky = computed(() => {
    const val = this.form.get('data_usage_change_percent')?.value;
    // Highlight if data usage jumped by over 200%
    return val !== null && val > 200;
  });

  constructor() {
    // Re-evaluate signals on form change
    this.form.valueChanges.subscribe(() => {
      // Angular signals update automatically if they depend on other signals, 
      // but here we are reading form values directly in the template getters 
      // or we can force update if we used signals for form state.
      // The getter approach in template is reactive enough for this simple case 
      // combined with change detection.
    });
  }

  analyze() {
    if (this.form.invalid) return;
    
    this.isAnalyzing.set(true);
    this.result.set(null);

    this.service.predictSingle(this.form.value).subscribe({
      next: (res) => {
        this.result.set(res);
        this.isAnalyzing.set(false);
      },
      error: () => this.isAnalyzing.set(false)
    });
  }

  resetForm() {
    this.form.reset({
      distance_change: 0,
      time_since_sim_change: 100,
      current_city: 'Colombo',
      previous_city: 'Colombo',
      is_roaming: false,
      sim_change_flag: false
    });
    this.result.set(null);
  }
}