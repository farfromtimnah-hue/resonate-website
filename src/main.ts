import './styles/tokens.css';
import './styles/base.css';
import './styles/wordmark.css';
import './styles/scenes.css';
import './styles/video.css';
import { initLang } from './lang';
import { initScroll } from './scroll';
import { initHeroScenes, initReveals } from './scenes/hero';

initLang();
initScroll();
initHeroScenes();
initReveals();
