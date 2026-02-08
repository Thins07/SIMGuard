import { Component, output } from '@angular/core';

@Component({
  selector: 'app-hero',
  standalone: true,
  template: `
    <div class="relative overflow-hidden h-full flex items-center justify-center bg-slate-950">
      <!-- Background Effects -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-7xl pointer-events-none">
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-teal-600/10 rounded-full blur-3xl"></div>
        <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl"></div>
      </div>

      <div class="relative max-w-4xl mx-auto px-4 text-center sm:px-6 lg:px-8">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-700 text-sm text-teal-400 mb-8 animate-fade-in-up">
          <i class="fas fa-check-circle"></i>
          <span>Final Year Project 2025</span>
        </div>

        <h1 class="text-4xl sm:text-6xl font-extrabold tracking-tight text-white mb-6 animate-fade-in-up delay-100">
          AI-Driven Detection of <br/>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-500">
            SIM Swapping Attacks
          </span>
        </h1>

        <p class="text-lg sm:text-xl text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed animate-fade-in-up delay-200">
          Analyze user behavior analytics and device forensics to detect anomalies in real-time. 
          Protect user identities from unauthorized SIM porting.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in-up delay-300">
          <button (click)="start.emit()" class="w-full sm:w-auto px-8 py-4 bg-teal-500 hover:bg-teal-400 text-slate-900 font-bold rounded-xl shadow-lg shadow-teal-500/25 transition-all duration-200 transform hover:scale-105 flex items-center justify-center gap-2">
            <i class="fas fa-radar"></i>
            Start Detection
          </button>
          
          <a href="#" class="w-full sm:w-auto px-8 py-4 bg-slate-800 hover:bg-slate-700 text-white font-semibold rounded-xl border border-slate-700 transition-all duration-200 flex items-center justify-center gap-2">
            <i class="fas fa-book"></i>
            Read Thesis
          </a>
        </div>

        <!-- Features Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 animate-fade-in-up delay-500 text-left">
          <div class="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-sm">
            <div class="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center mb-4 text-teal-400 text-xl">
              <i class="fas fa-brain"></i>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">AI Detection</h3>
            <p class="text-slate-400 text-sm">Uses XGBoost and CatBoost models to classify suspicious behavior patterns.</p>
          </div>
          <div class="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-sm">
            <div class="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center mb-4 text-blue-400 text-xl">
              <i class="fas fa-fingerprint"></i>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">Device Forensics</h3>
            <p class="text-slate-400 text-sm">Analyzes IMEI, IMSI, and Location Area Identity (LAI) changes.</p>
          </div>
          <div class="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-sm">
            <div class="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center mb-4 text-purple-400 text-xl">
              <i class="fas fa-file-contract"></i>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">Forensic Reports</h3>
            <p class="text-slate-400 text-sm">Generates PDF reports for law enforcement and ISP investigation.</p>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in-up {
      animation: fadeInUp 0.8s ease-out forwards;
      opacity: 0;
    }
    .delay-100 { animation-delay: 0.1s; }
    .delay-200 { animation-delay: 0.2s; }
    .delay-300 { animation-delay: 0.3s; }
    .delay-500 { animation-delay: 0.5s; }
  `]
})
export class HeroComponent {
  start = output<void>();
}