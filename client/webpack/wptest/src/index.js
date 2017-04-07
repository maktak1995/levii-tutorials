import './styles.scss';

// アンカー(a)があれば、Buttonコンポーネントをそこに描画します
if (document.querySelectorAll('a').length) {
    require.ensure([], () => {
        //(訳注: 元記事には末尾の.defaultがありませんでした。これが無いと動作しない?)
        const Button = require('./Components/Button').default;
        const button = new Button('google.com');
        button.render('a');
    }, 'button');
}
// タイトル(h1)があれば、Headerコンポーネントをそこに描画します
if (document.querySelectorAll('h1').length) {
    require.ensure([], () => {
        //(訳注: 元記事には末尾の.defaultがありませんでした。これが無いと動作しない?)
        const Header = require('./Components/Header').default;
        new Header().render('h1');
    }, 'header');
}
