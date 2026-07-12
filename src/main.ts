import './styles/tokens.css';
import './styles/base.css';
import './styles/wordmark.css';
import './styles/scenes.css';
import './styles/video.css';
import './styles/split.css';
import './styles/proof.css';
import { initLang } from './lang';
import { initScroll } from './scroll';
import { initHeroScenes, initReveals } from './scenes/hero';
import { initProofScenes } from './scenes/proof';

initLang();
initScroll();
initHeroScenes();
initProofScenes();
initReveals();
