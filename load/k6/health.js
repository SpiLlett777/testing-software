import http from 'k6/http';
import {check, sleep} from 'k6';

export const options = {
    vus: Number(__ENV.VUS || 10),
    duration: __ENV.DURATION || '30s',
    thresholds: {http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<500'], checks: ['rate==1']},
};

export default function () {
    const response = http.get(`${__ENV.BASE_URL || 'http://127.0.0.1:5000'}/api/health`);
    check(response, {
        'status 200': r => r.status === 200,
        'JSON status ok': r => {
            try {
                return r.json('status') === 'ok';
            } catch {
                return false;
            }
        },
    });
    sleep(0.1);
}

export function handleSummary(data) {
    return {[__ENV.SUMMARY_PATH || 'artifacts/lab08/summary.json']: JSON.stringify(data, null, 2)};
}
