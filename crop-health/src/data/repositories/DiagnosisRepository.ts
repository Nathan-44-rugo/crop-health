// src/data/repositories/DiagnosisRepository.ts

import * as mime from 'react-native-mime-types';
import { DiagnosisRepository } from '../../domain/repositories/DiagnosisRepository';
import { DiagnosisResult } from '../../domain/entities/DiagnosisResult';
import { BACKEND_URL } from '../../../config';

export class DiagnosisRepositoryImpl implements DiagnosisRepository {
  private api = BACKEND_URL;

  async diagnose(imageUri: string): Promise<DiagnosisResult> {
    const fileName = imageUri.split('/').pop()!;
    const type = mime.lookup(fileName) || 'image/jpeg';

    const formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      name: fileName,
      type,
    } as any);

    // 🔁 Use fetch() instead of axios
    const resp = await fetch(`${this.api}/diagnose`, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
      },
      body: formData,
    });

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`HTTP ${resp.status}: ${text}`);
    }

    const data = await resp.json();

    return {
      diseaseName: data.disease_class,
      confidence: data.confidence,
      treatmentAdvice: data.treatment_advice,
      logId: data.log_id,
    };
  }
}
