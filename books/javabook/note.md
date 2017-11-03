## 2. 基本的な書き方を身につける

- 修飾子
	- `transient`
		- フィールドをシリアライズ対象から除外
		- オブジェクトのファイル保存、ネットワーク送受信時などに不要になる一時データをシリアライズしなくて済む
	- `volatile`
		- マルチスレッドからアクセスされるフィールドに対して、スレッドごとに値がキャッシュされないようにする
		- スレッドセーフのため
	- `synchronized`
		- メソッドまたはブロックの同期
		- 同時に1つのスレッドからしかアクセスされないことが保証される
	- `native`
		- メソッドがネイティブコード（C/C++で書かれたDLL, 共有ライブラリなど）を呼び出す
	- `strictfp`
		- クラス、インタフェース、メソッドで浮動小数点数をIEEE 754規格で厳密に処理する
		- 厳密な浮動小数点演算によって、プラットフォーム間の移植性向上
- 変数名の後ろに `_` をつけるのはもはや不要
	- IDEで書くのが当たり前なので、フィールドとローカル変数の名前が一緒でも区別がつく
	- フレームワークによっては末尾の `_` によって変数のバインドに失敗するものもある
- 変数は名詞、メソッドは動詞で命名
	- booleanの変数名に `isXxx` とつけるのは違う
	- 変数名は `xxx` で、問い合わせるメソッドが `isXxx` と命名されるべき

## 3. 型を極める

- プリミティブ型
	- 桁数の多い数字はアンダースコアで区切りを表現できる：`long amount = 123_456_789L;`
	- Widening（ワイドニング；型のデータサイズが大きくなるような自動変換）は整合性が保たれる
		- e.g., short -> int
	- 逆に Narrowing（ナローイング）はコンパイルエラー (e.g., int -> short)
		- キャストすればコンパイルは通るけど、値はおかしくなる：`short shortNum = (short) intNum`
- 参照型
	- Wrapper Class：プリミティブ型を内包し、そのプリミティブ型の値を操作する機能を備えたもの
		- int <-> Integer, double <-> Double, ...
		- `Integer.MAX_VALUE`, `Float.MIN_VALUE`, ...
	- プリミティブ型からラッパークラスへの変換は、`valueOf`を使うと-127~128の範囲では事前に生成されたオブジェクトが利用できるので、メモリに優しい
	- プリミティブ型のintの初期値は0だが、ラッパークラスではNULL
		- ゼロとNULLを区別したいときはラッパークラスを使う
			- HTTP通信で取得した値やファイルから読み込んだ値のストアなど
	- Autoboxing: Primitive -> Wrapper Classへの変換 `Integer numInt = 10`
	- Unboxing: Wrapper Class -> Primitiveへの変換 `10 + Integer.valueOf(10)`
		- 依存しすぎると、ラッパークラスを誤って `==` で比較してしまってFalseになる、といったミスが発生する
			- -128 ~ 127の値をautoboxingしたオブジェクトだけは、事前に生成されたオブジェクトを使うので例外的に一致する
		- というわけで
			1. 原則としてautoboxing, unboxingは使用せず、明示的に変換
			2. ファイル、DB、HTTPリクエストなどの結果得られる値を保持する場合はラッパークラス
			3. 数値計算はプリミティブ型
			4. 記述量の削減（型変換を明記しないこと）が効果的な場合に限り、autoboxing, unboxingを利用
- クラス
	- 慣例として、他者が提供するライブラリやフレームワークなどとパッケージ名が重複してしまわないよう、自分が所有しているドメイン名を逆にしたものからパッケージ名を始める
	- フィールド、メソッドの修飾子は指定しないとパッケージプライベート（同一パッケージ内のクラスからのみ参照可能；`protected`はそれに加えて子クラスからも参照可能）
	- インタフェース
		- 絶対publicになるが、著者は省略せずに `public interface` とかく
		- メソッド定義のみで、処理は記述できない
			- が、Java8からは処理内容を定義する `default` メソッドが追加された
		- 匿名クラス
			- `public interface TaskHandler { ... }` -> `TaskHandler taskHandler = new TaskHandler() { ... };`
			- クラスを特定の一箇所で使うだけなら、 `implement` した名前のあるクラスを定義するよりもかんたん
	- nested class の使い方はEffective Java参照
- オブジェクトの等価性
	- `public boolean equals(Object obj)`
		- フィールドの値に基づく比較（値を1つずつ比較するので時間がかかる）
	- `public int hashCode()`
		- 同じオブジェクトなら同じハッシュ値を返す
		- ハッシュ値が異なれば異なるオブジェクト
		- 異なるオブジェクトでもハッシュ値が異なることはある
		- （intの値の比較だけなので高速）
	- `HashMap` や `HashSet` では、
		1. 最初にハッシュ値でオブジェクトを比較
		2. ハッシュ値が一致した場合に限り、`equals()`で厳密に値の一致判定
	- `equals()` と `hashCode()` の両方で等価だと判断されないと、オブジェクトはイコールにならない
		- 両メソッドはEclipseだとフィールドに基づいて自動生成される
		- `Objects.hash(v1, v2, ...)` を使えばハッシュ値生成簡単
- `enum`
	- `public static final` による定数は型安全ではない
		- `String COLOR_RED`, `String COLOR_GREEN`, `String COLOR_BLUE` のいずれかを取りたいメソッドを書くとき、引数の型はただの `String` になるので、 `"aaa"` のような意図しない入力も受け付けてしまう
		- 定数をコンパイルした結果はただの値； `String s = COLOR_RED` でも、コンパイル結果は `String s = "red"`
	- なので、`enum`型でいくつかの定数の集まりを表現する
		```
		public enum Color {
			RED, GREEN, BLUE
		};
		```
		- すると、`setColor(Color c)` のような、想定した値以外は受け付けない型安全な定数利用が可能
	- フィールドやメソッドの定義も可能
		```
		public enum HttpStatus {
			OK(200), NOT_FOUND(404), INTERNAL_SERVER_ERROR(500);

			private final int value;

			private HttpStatus(int value) { // enum のコンストラクタは private
				this.value = value;
			}
			public int getValue() {
				return value;
			}
		}
		```
- ジェネリクスで様々な型を受け付ける汎用的なクラス・メソッド定義

## 4. 配列とコレクションを極める

### 配列

- プリミティブ型は0初期化、ラッパークラス（オブジェクト）ではNULL初期化
- `int[] ary` でも `int ary[]` でもいいけど、『○○型の配列』であることを明示するために `int[]` をおすすめ
- 宣言時に内容が決まっていなければ `new int[10]` で初期化するが、書写はこの場合コレクションを利用することのほうが多い
- 宣言時の初期化は `int[] ary = {1, 2, 3}` or `int[] ary = new int[] {1, 2, 3}`；宣言済み配列への代入（引数含む）は後者のみ可能
- 要素数の変更は `Arrays.copyOf` で新規作成＆コピーするが、そもそも要素数可変なら最初からコレクションを利用したい
- `Arrays.sort` でソート
	- プリミティブ型：値の昇順
	- オブジェクト：ComparableインタフェースのcompareToメソッドで並び替え
		- Comparatorを引数に渡してソートするか、対象のクラスをComparableインタフェースのimplementsとして定義してcompareToメソッドを実装するか、2種類選べる
		- しかし後者は「そのクラスがもつデフォルトの並び順によるソート」を定義するので、最も自然な並びであるべきで、しかしそれは自明ではない
		- 多くのクラスは業務上の要件によって“自然な並び”の定義が異なるので、Comparatorを使ったソートを使うことがほとんど
- サーチ
	- 同じデータに対して何度も探索するなら、ソート→バイナリサーチ
	- 一度だけなら線形探索など、バイナリサーチ以外の方法で
- 可変長引数
	- `void log(String message, String... args)`

どのコレクションインタフェース `List`（インデックスを指定して値を取得、設定をしたい）, `Set`（要素に重複がなく、検索・ソートを高速にしたい）, `Map` (key-value pair) を決めたら、どの実装を選ぶかを検討する：

### List

- Listを for-each と iterator のどちらで探索するか？
	- 要素に対する操作（削除、更新）も行いたい時は iterator
- `ArrayList`
	- **forなどをつかった全体的な繰り返し処理向き**
	- 内部に配列を保持していて、そのサイズは何も指定しないと10
	- このサイズを超えるとき、「よりサイズの大きい配列を新たに生成して、元の配列から全要素をコピーする」処理が発生して非効率
	- 要素数の目安が事前についているのなら、コンストラクタでそれを設定したほうが無駄な配列生成＆コピー処理が削減できる
	- インデックスを指定した要素の代入・取得は高速
	- 配列なので、リストの途中の要素の代入・削除はおそい
- `LinkedList`
	- **配列をiterateしつつ、途中で要素の追加/削除を行うとき**
	- 初期サイズの概念はない
	- ArrayListとは逆で、インデックスを指定した要素の代入・取得は時間がかかる
	- 最初から順番に（＝iterator通りに）舐める処理でアドバンテージ
- `CopyOnWriteArray`
	- **複数のスレッドから同時にアクセスしても正しく処理される**ArrayList の拡張
	- ループ実行時に元のリストをコピーして、そのリストに対してループを実行する
	- なのでオリジナルの値は一定で、スレッドからの同時アクセスによるConcurrentModificationExceptionが防げる
	- 性能はほぼArrayListと同等だが、ループや要素の追加・変更・削除時には内部的な配列のコピーが発生するので、その分遅くなる

### Map

- `HashMap`
	- キーの `hasCode` メソッドでハッシュ値計算→ハッシュテーブルのサイズで割った余りをインデックスにする
		- 当然衝突することもあるので、内部的にはLinkedListのような構造の場所にキーと値のペアを格納していて、衝突時は末尾に追加
	- 値を取り出すとき、同一インデックスに複数のEntryがあれば先頭から順に `equals` で比較しながら一致するkey-valueペアをlookup
	- ハッシュテーブルの初期サイズは16で、要素数がその75％に達するとサイズを自動で拡張する
		- サイズ <<< 要素数 だとハッシュ値の競合が増えてloopupに時間がかかるようになるため　
	- 要素の追加順序は保持されないので、イテレータは追加時とは異なる順番
	- **次の3つが適さない、その他の場合に使う**
- `ConcurrentHashMap`
	- **複数スレッドから同時にアクセスする場合**
	- ハッシュテーブルの拡張と要素の追加が同時に起こると無限ループになりうるので、atomicに複数スレッドからの処理をさばく
	- `synchronized` を使うのも手
- `LinkedHashMap`
	- **要素の追加順序を保持したいとき**
	- HashMapのサブクラスで、要素が前後のリンクをもつ
	- リンクの付け替えオーバーヘッドがあるが、HashMapとほぼ変わらない性能
	- HashMapはハッシュ値計算→重複時にリストの列挙が発生するので、全要素の列挙ならこちらのほうが高速
- `TreeMap`
	- **キーの大小を意識するとき**
	- Binary Search Treeを使うので、要素の追加・削除・検索はO(logn)
		- 頻繁に追加・削除・検索をするとHashMapなど他のMapと比較して処理時間の差が顕著に出る

### Set

- 内部的にはMapを持っていて、キーだけを使っているのがSet
	- 値は null 以外ならなんでもいいけど、通常は true
- なので実装、使い分けはMapと同じ
	- `HashSet`
	- `LinkedHashSet`
	- `TreeSet`
- ConcurrentHashSet は存在しない
	- `Collections.newSetFromMap()` で ConcurrentHashMap からセットが作れるので

### その他

- `Queue`
	- バッファ（データの一時保存場所；通信処理などで使う）として使われる
	- マルチスレッドだと異なるスレッドが保存・取り出しを行うので、スレッドセーフな Blocking Queue を使う必要アリ
- `Dequeue`
	- 双方向の値の出し入れが可能なQueue
	- 筆者は使うことはほぼ無い

## 5. ストリーム処理を使いこなす

- Java8から：ラムダ式とStream API
- Stream API
	- **ストリームの作成** (collection, array -> stream)
	- **中間操作**（filterなど；stream -> stream）
	- **終端操作**（forEachによる出力など；stream -> collection, array, element-wise process, aggregate）
- ラムダ式
	- Comparatorが簡単にかける
		- Comparatorのcompareメソッドのように、実装すべきメソッドが1つしか無いインタフェース（関数型インタフェース）はラムダ式で記述可能
	- 引数の丸括弧、型、中身が省略可能な場合も
	- 処理が1つならreturn, 波カッコ, セミコロンも省略可能
	- メソッド参照
		- `list.forEach(System.out::println)` は `list.forEach(s -> System.out.println(s))` と同じ
		- 引数の数と型が一致していれば、処理の内容としてメソッドそのものを代入できる
		- `{インスタンス/クラス名}::{メソッド名}`、`this::{メソッド名}`
- streamの作成
	- `list.stream()`
	- `Arrays.stream(array)`
	- Mapの場合はEntrySetを取得してから、そのSetのStreamメソッドを呼び出すことで生成
		- `map.entrySet().stream().forEach(e -> /* something for e.getKey() and e.getValue() */)`
	- 数値レンジ
		- `IntStream.range(1, 5)` 末尾含まず
		- `IntStream.rangeClosed(1, 5)` 末尾含む
			- 同様に `LongStream`, `DoubleStream` も
- 中間操作
	- 要素を置き換える `map` 系いろいろ
		- `mapToInt`, `mapToDouble`, `mapToLong` にすると、戻り値が数値ストリームになるので、その後でsumやaverageのような数値処理メソッドが使える
		- `flatMap` は、`map` だと『Xのリストのストリーム』になるものが、flattenして『Xのストリーム』になる
	- 要素を絞り込む
		- `filter`, `limit`, `distinct`
	- `sorted` comparatorを渡してソートできる
- 終端操作
	- `forEach` で各要素に対するアクション実行
	- `collect(Collectors.xxx)`, `toArray`, `reduce` で結果をコレクションや数値としてまとめて返す
	- `findFirst`, `findAny`, `min`, `max` で1要素を取り出す
		- `min`, `max` は引数にcomparatorを
	- 集計 `count`, `min`, `max`, `sum`, `average`
		- 数値ストリームに対してのみ有効
		- `min`, `max` の引数不要
- Stream APIの中でも `map`, `filter`, `collect` は特によく使う
- ラムダ式という意味では、Java8から増えたListの `removeif(v -> xxx)`, `replaceAll(v -> xxx)` や、Mapの `compute`, `computeIfPresent`, `computeIfAbsent` も覚えておくと良い
- Listの初期化にStream APIが使える
	- `IntStream.of(1, 2, 3, 4).boxed().collect(Collectors.toList())`
	- `IntStream.range(0, 10).boxed().collect(Collectors.toList())`
		- `boxed()` で int -> Integer のboxing
	- `Stream.of("AAA", "BBB", "CCC").collect(Collectors.toList())`
- 配列の初期化でも使える
	- `Integer[] array = IntStream.of(1,2,3,4).boxed().toArray(n -> new Integer[n])`

## 6. 例外を極める

- 大きく分けて3種類の例外
	- 検査例外 (Exception) `java.lang.Exception`
		- コンパイルエラーになるような、プログラム作成時に予測できる例外
		- `throws` 句をメソッドシグネチャにつけてプログラム側での補足（try-catch）を強制
		- 筆者はミッションクリティカルなエンプラシステムを扱うことがあるので、たとえコードが長大化しても賛成
	- 実行時例外 (Runtime Exception) `java.lang.RuntimeException`
		- 誰も補足しなければ、（スレッドを開始した）Java VMまで例外が伝搬されてスレッドが終了する
	- エラー (Error) `java.lang.Error`
		- システムを継続できない致命的なもの e.g., OOM
		- プログラムで補足すべきではない
- tryブロックの中の処理は最小限に
- リソースの解放漏れを防ぐ
	- Java 6 まで：try ~ catch ~ finally の finally で
	- Java 7 から：try-with-resources構文
		- `try (InputStream is = File.newInputStream(path); ...) { ~ } catch { ~ }`
		- tryの中でAutoClosableインタフェースの実装クラスを宣言すれば、終了時に勝手にcloseしてくれる
- 同様にハンドリングしたい例外はマルチキャッチする `catch (XxxException | YyyException e) { ~ }`
- なにかあったときにエラーコードをreturnしないで、きちんとJavaの例外機構を使う
	- Cのように例外機構を言語仕様として定めていない場合はいいけど、Javaはそれがあるから、失敗したらきちんと例外を発する
	- ただし、何でもかんでもthrowすればいいというわけでもない；`isXxx()`というメソッドはbooleanを戻すことが明らかなので、throwせずfalseを返せばいいかもしれない
- catchした例外をもみ消さない（catch内で何かしらの処理をする）
	- ログ出力（スタックトレースなど）
	- 処理の継続判定
		- オブジェクトが存在しないことをcatchしてログに出すだけだと、あとで再びそれを参照してNPEになるだけ
		- catchしたらデフォルト値を設定してあげるか、そこで処理を終了するか
- `throws Exception` はNG
	- すべての呼び出し元で `throws Exception` をしなければならない＆それにもかかわらず全ての具体的な例外がそれに巻き込まれる
	- どうしてもExceptionを補足しなければならないときはある
		- 依存ライブラリが `throws Exception` してる←独自の例外でラップしてしまうのも手
		- スレッドプール内のワーカースレッドなど、どんな例外があっても常に処理を継続させたい場合
- どの部分で例外を補足・処理すべきか
	1. 例外が発生する（可能性のある）箇所
		- たいていは末端の処理で、数が多く、そこで個別に例外をハンドリングするのは全体の流れを見づらくするだけ
		- なので、例外は発生させるだけに留める
	2. 処理の流れを判断する箇所
		- ここで例外を補足し、処理の終了・継続を判断する
		- 大きなシステムなら、補足する階層はできるだけ上位がいい；どこで補足するかはプログラム設計段階で認識を合わせておきたい
- 独自例外
	- 独自に、様々な例外たちを統一的に扱いたい場合につくる
	- 親のException, RuntimeExceptionには引数を取らない場合もあるが、独自例外では引数強制にして意味のある例外にすべき
	- 筆者のおすすめはメッセージの代わりにエラーIDとパラメータをとる例外
		- 実際のメッセージを『エラーIDに対応する情報』として例外定義の外に追い出せる
		- プログラマごとにエラーメッセージが違う（けどコンテキストは同じ）という状況が回避できる
		- メッセージ生成はログ出力クラスや例外ハンドラで行う
- 例外のトレンド
	1. ExceptionよりRuntimeException
		- フレームワークの独自例外はだいたいRuntimeException
		- プログラム開始部分に近い共通部分でまとめて例外処理をさせたいねらい
	2. ラムダ式の中で発生した例外の扱い
		- ラムダ式内で発生した実行時例外はラムダ式の外側に例外が伝わり、それを補足できる
		- ただし、処理する要素ひとつひとつが発した例外すべてを受け取れるわけではないので、「処理する要素次第でコケることもある」というときはラムダ式の内側で例外を補足したほうがよい
	3. Java8から導入されたOptionalクラスによる、nullチェックからの解放＆NPEの抑止
		- ただ、Optionalは`isPresent()`による値の存在確認が必須になり、nullチェックと手間が変わらない説
			- nullチェック：開発者の注意次第
			- Optional：オブジェクトを返す側で、値が存在する場合と存在しない場合、それぞれのコードを書くことを開発者に強制できる

## 7. 文字列操作を極める

- 文字列の結合：StringBuilderでappend, +, "xxx".concat("yyy")
	- ループで繰り返し結合するときは、StringBuilder.appendが圧倒的に早い
		- +やconcatはループ毎に文字列オブジェクト生成処理を繰り返している
		- `"xxx" + "yyy"` はコンパイラによって `new StringBuilder(String.valueOf("xxx").append("yyy")).toString()` に変換されるが、これをループしても毎回無駄にStringBuilderと文字列オブジェクトが生成されるのでパフォーマンス低
	- StringBuilderのスレッドセーフ版、StringBufferもある
- Java8からは `String.join()` が標準
- 分割・置換のStringクラス使用vs正規表現
	- 一度だけならStringクラスのメソッドをつかって簡潔にかけばいい
	- 大量の文字列に対して何回もやるなら、事前に正規表現オブジェクトを生成して使いまわす
- 「デプロイしたら文字化けする」問題にはまらないために、（特にサーバサイドJavaの開発では）デフォルトエンコーディングを使わないよう意識することが大切
	- 引数なしでStringコンストラクタやStringクラスの `getBytes` を使ったり、FileReader, FileWriterなどを使うとデフォルトエンコーディングになってしまう
		- 必ず引数でcharset, エンコーディングを指定する or エンコーディング指定オプションのあるメソッドで代替する
	- サロゲートペア（2文字で1文字を表現したやつ）の扱い
		- 禁止するなら `Character.isLowSurrogate(c)` や `Character.isHighSurrogate(c)` で確認してエラーを出せばいい
		- 許容するなら、文字数カウントなどで注意が必要
			- `str.length()` よりも `str.codePointCount(0, str.length())` つかったり
	- 文字列比較は equals を使わないと、同じ中身でもオブジェクトとしては別になってしまう
		- `"aaa"` と `"a" + "aa"` は文字列としては同じ、でも `==` で比較すれば false
		- `("a" + "aa").intern()` とすれば、明示的に両者を同一オブジェクトとして扱える