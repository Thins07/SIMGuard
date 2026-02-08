import { Component, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SimGuardService } from '../services/simguard.service';
import { RiskChartComponent } from './risk-chart.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RiskChartComponent],
  template: `
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h2 class="text-2xl font-bold text-white">Detection Results</h2>
          <p class="text-slate-400 text-sm mt-1">
            Analysis Timestamp: {{ results()?.analysis_timestamp | date:'medium' }}
          </p>
        </div>
        <button 
          (click)="downloadReport()"
          class="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white rounded-lg transition-colors font-medium text-sm">
          <i class="fas fa-file-pdf text-red-400"></i>
          Download Investigation Report
        </button>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <!-- Processed -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div class="flex items-center gap-3 mb-2">
            <div class="p-2 bg-blue-500/10 rounded-lg text-blue-400"><i class="fas fa-database"></i></div>
            <span class="text-slate-400 text-sm font-medium">Processed</span>
          </div>
          <div class="text-3xl font-bold text-white">{{ results()?.summary?.total_records }}</div>
          <div class="text-xs text-slate-500 mt-1">Rows analyzed</div>
        </div>

        <!-- Suspicious -->
        <div class="bg-slate-900 border border-red-500/30 p-5 rounded-xl relative overflow-hidden">
          <div class="absolute right-0 top-0 w-24 h-24 bg-red-500/10 rounded-bl-full -mr-4 -mt-4"></div>
          <div class="flex items-center gap-3 mb-2">
            <div class="p-2 bg-red-500/10 rounded-lg text-red-400"><i class="fas fa-exclamation-triangle"></i></div>
            <span class="text-red-200 text-sm font-medium">Suspicious</span>
          </div>
          <div class="text-3xl font-bold text-white">{{ results()?.summary?.suspicious_count }}</div>
          <div class="text-xs text-red-300/50 mt-1">Potential threats detected</div>
        </div>

        <!-- Safe -->
        <div class="bg-slate-900 border border-teal-500/30 p-5 rounded-xl">
          <div class="flex items-center gap-3 mb-2">
            <div class="p-2 bg-teal-500/10 rounded-lg text-teal-400"><i class="fas fa-check-circle"></i></div>
            <span class="text-teal-200 text-sm font-medium">Clean</span>
          </div>
          <div class="text-3xl font-bold text-white">{{ results()?.summary?.clean_count }}</div>
          <div class="text-xs text-teal-500/50 mt-1">Verified safe activities</div>
        </div>

        <!-- Users -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl">
           <div class="flex items-center gap-3 mb-2">
            <div class="p-2 bg-purple-500/10 rounded-lg text-purple-400"><i class="fas fa-users"></i></div>
            <span class="text-slate-400 text-sm font-medium">Unique Users</span>
          </div>
          <div class="text-3xl font-bold text-white">{{ results()?.summary?.users_analyzed }}</div>
          <div class="text-xs text-slate-500 mt-1">Entities tracked</div>
        </div>
      </div>

      <!-- Chart & Table Layout -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Risk Distribution Chart -->
        <div class="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center">
          <h3 class="text-lg font-semibold text-white mb-6 w-full">Risk Distribution</h3>
          @if (results()) {
            <app-risk-chart [data]="results()!.risk_distribution"></app-risk-chart>
          }
          <div class="w-full mt-6 space-y-3">
             <div class="flex justify-between items-center text-sm">
                <span class="flex items-center gap-2 text-slate-300"><span class="w-3 h-3 rounded-full bg-red-500"></span> High Risk</span>
                <span class="font-bold text-white">{{ results()?.summary?.high_risk_users }}</span>
             </div>
             <div class="flex justify-between items-center text-sm">
                <span class="flex items-center gap-2 text-slate-300"><span class="w-3 h-3 rounded-full bg-amber-500"></span> Medium Risk</span>
                <span class="font-bold text-white">{{ results()?.summary?.medium_risk_users }}</span>
             </div>
             <div class="flex justify-between items-center text-sm">
                <span class="flex items-center gap-2 text-slate-300"><span class="w-3 h-3 rounded-full bg-teal-500"></span> Low Risk</span>
                <span class="font-bold text-white">{{ results()?.summary?.clean_users }}</span>
             </div>
          </div>
        </div>

        <!-- Suspicious Activities Table -->
        <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col">
          <div class="p-6 border-b border-slate-800">
            <h3 class="text-lg font-semibold text-white">Suspicious Activities</h3>
          </div>
          
          <div class="overflow-x-auto flex-1">
            <table class="w-full text-left text-sm text-slate-400">
              <thead class="bg-slate-950 text-slate-200 uppercase font-medium text-xs">
                <tr>
                  <th class="px-6 py-3">Timestamp</th>
                  <th class="px-6 py-3">User ID</th>
                  <th class="px-6 py-3">Risk</th>
                  <th class="px-6 py-3">Reason</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800">
                @for (item of results()?.suspicious_activities; track $index) {
                  <tr class="hover:bg-slate-800/50 transition-colors">
                    <td class="px-6 py-4 whitespace-nowrap">{{ item.timestamp }}</td>
                    <td class="px-6 py-4 font-mono text-xs text-white">{{ item.user_id }}</td>
                    <td class="px-6 py-4">
                      <span 
                        class="px-2 py-1 rounded text-xs font-bold"
                        [class]="getRiskClass(item.risk_level)">
                        {{ item.risk_level }}
                      </span>
                    </td>
                    <td class="px-6 py-4 max-w-xs truncate" title="{{ item.flag_reason }}">
                      {{ item.flag_reason }}
                    </td>
                  </tr>
                }
                @if (!results()?.suspicious_activities?.length) {
                   <tr>
                     <td colspan="4" class="px-6 py-8 text-center text-slate-500">
                       No suspicious activities detected.
                     </td>
                   </tr>
                }
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  `
})
export class DashboardComponent {
  service = inject(SimGuardService);
  results = computed(() => this.service.analysisData());

  getRiskClass(level: string): string {
    switch (level.toUpperCase()) {
      case 'HIGH': return 'bg-red-500/20 text-red-400';
      case 'MEDIUM': return 'bg-amber-500/20 text-amber-400';
      case 'LOW': return 'bg-teal-500/20 text-teal-400';
      default: return 'bg-slate-700 text-slate-300';
    }
  }

  downloadReport() {
    window.open(this.service.getReportUrl(), '_blank');
  }
}