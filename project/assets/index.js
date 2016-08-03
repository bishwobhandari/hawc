import textCleanupStartup from 'textCleanup';
import robVisualStartup from 'robVisual';
import robTableStartup from 'robTable';
import bmdStartup from 'bmd';
import {BMDLine} from 'bmd/models/model.js';

import { renderCrossStudyDisplay } from 'robTable/components/CrossStudyDisplay';
import { renderRiskOfBiasDisplay } from 'robTable/components/RiskOfBiasDisplay';
import { renderStudyDisplay } from 'robTable/components/StudyDisplay';
import nestedTagEditorStartup from 'nestedTagEditor';


window.app = {
    textCleanupStartup,
    robVisualStartup,
    robTableStartup,
    renderCrossStudyDisplay,
    renderRiskOfBiasDisplay,
    renderStudyDisplay,
    bmdStartup,
    BMDLine,
    nestedTagEditorStartup,
};
