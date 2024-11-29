# Changelog

All notable changes to this project will be documented in this file.

## [v1.6.0-beta](https://github.com/FlysonBot/Mastermind/releases/tag/v1.6.0-beta) - 2024-11-28

Fix install issue. Now should work normally following the instruction on README.md

### 🚀 Features

- **(workflow)** Add ruff formatter and linter *([e407850](https://github.com/FlysonBot/Mastermind/commit/e407850c447cb05ad4a376c8fea00491f1d9f0f6))*

### 🐛 Bug Fixes

- Outdated tests *([03ed312](https://github.com/FlysonBot/Mastermind/commit/03ed3124ba0048de97d448043d3b7786f30f0d7a))*
- Project requires python v3.9 rather than v3.8 becuase pandas requires v3.9 *([5f29ccb](https://github.com/FlysonBot/Mastermind/commit/5f29ccbdaa32ea5951af6e69c3e85f99c05b5cbd))*
- Project require python 3.10 not 3.9 *([ea9ae1d](https://github.com/FlysonBot/Mastermind/commit/ea9ae1d6e804b40c8d6ad6eaf4b9cc072e5517fb))*
- Metadata generating error setup.py *([16db319](https://github.com/FlysonBot/Mastermind/commit/16db319ed84fb6a6fa6f49884f51e07a14fc23f0))*
- Main.py missing function main *([ae1f412](https://github.com/FlysonBot/Mastermind/commit/ae1f412da223d2610e20f29a535cbb95c9791aa6))*

### 💼 Other

- Update setup.py *([c9e367d](https://github.com/FlysonBot/Mastermind/commit/c9e367d03ae61b106e1720b07a34680c47103421))*

### 🚜 Refactor

- Small refactoring from pull request review *([970bcde](https://github.com/FlysonBot/Mastermind/commit/970bcde02af907f4e040ba9fcd8b35dad35696e7))*
- Change /src to /src/mastermind *([6531ffa](https://github.com/FlysonBot/Mastermind/commit/6531ffa2f4428919b28f66c799239c6cc01d115f))*

### 📚 Documentation

- Update sphinx documentation *([18d276f](https://github.com/FlysonBot/Mastermind/commit/18d276f14eb4675b28a43d3d62bedfc83990386f))*

### 🎨 Styling

- Ruff format and lint *([75b789f](https://github.com/FlysonBot/Mastermind/commit/75b789f26c28c0bd47b2447ccb760481a2c8e594))*
- Ruff format and lint *([8d5a628](https://github.com/FlysonBot/Mastermind/commit/8d5a628723c19b26fd8435e28e29a10e76c2d7b1))*
- Apply Ruff *([ad57115](https://github.com/FlysonBot/Mastermind/commit/ad571153af8f103719782e59c9c963933aa61be0))*
- Apply ruff lint and format *([6e2a3ed](https://github.com/FlysonBot/Mastermind/commit/6e2a3edecf71aeb11e0987d195ec154db606f09a))*

### 🧪 Testing

- **(menu)** Add abstract method test for data menu *([b8347a6](https://github.com/FlysonBot/Mastermind/commit/b8347a61d84b3de2b1b1e221bfdad79867de0b64))*
- **(validation)** Add more test *([9da2f57](https://github.com/FlysonBot/Mastermind/commit/9da2f571588c2468e95940e58201fb582ce29fd3))*

### ⚙️ Miscellaneous Tasks

- Fix typo in readme *([2940d8c](https://github.com/FlysonBot/Mastermind/commit/2940d8cea1c56029cd031316709f5499f4d2d17f))*
- Fix typo and grammar *([081b564](https://github.com/FlysonBot/Mastermind/commit/081b564bd9764feff3d04ef5be17b7a6414cd192))*
- Modify ruff config *([bcff791](https://github.com/FlysonBot/Mastermind/commit/bcff79134f4a11072182e8e9042964ca2df6008a))*
- Update ruff setting *([c6ffb72](https://github.com/FlysonBot/Mastermind/commit/c6ffb72a04580afd14e01208012ecd3afe70a3e7))*
- Add repo still under development notice *([fc00ac7](https://github.com/FlysonBot/Mastermind/commit/fc00ac7f40db3e6497ae5e733d342c04ed5cfd07))*
- Update ruff.yaml and rename to ci_automate.yaml *([759e54f](https://github.com/FlysonBot/Mastermind/commit/759e54f1d0d4abcf9e6778794f10b59789432744))*
- Fix malfunctioning ci_automate.yaml *([a0291c0](https://github.com/FlysonBot/Mastermind/commit/a0291c0a32884da864faabcdaf7eeca67a3bdf0e))*
- Change to use unittest instead *([844d709](https://github.com/FlysonBot/Mastermind/commit/844d709ec998d16c4a581585eafce83e3ccedda1))*
- Update .gitignore *([7509bdb](https://github.com/FlysonBot/Mastermind/commit/7509bdb6b83cd797e97bf2de0f0869ba25925885))*
- Fix broken unittest *([cbd74ac](https://github.com/FlysonBot/Mastermind/commit/cbd74ac43c044bddbae4a5601b457904c84009d6))*
- Add ruff pre-commit at server side *([4ff5177](https://github.com/FlysonBot/Mastermind/commit/4ff5177d96b4a238a79aca09f52278effc7bdcea))*

## [v1.5.1-beta](https://github.com/FlysonBot/Mastermind/releases/tag/v1.5.1-beta) - 2024-11-27

Fix bugs and made the package installable through pip with git. Ready to be use as a stable pre-release.

### 🚀 Features

- **(doc)** Tweak Sphinx to generate documentation *([1151a6f](https://github.com/FlysonBot/Mastermind/commit/1151a6f2febebed4ea40180fdd338dfa1700dcf1))*
- **(main)** Split classes into multiple files *([c96a2b4](https://github.com/FlysonBot/Mastermind/commit/c96a2b4696782ff1e49cd7abf9c4ccdd216fe7fc))*
- **(storage)** Add exception handling for when errors occured during unpickling. *([e0aad14](https://github.com/FlysonBot/Mastermind/commit/e0aad14ff2128a82ad97994d246a422968bead0d))*
- Unified interface for retrieving game history and continuable game *([aac41d5](https://github.com/FlysonBot/Mastermind/commit/aac41d570396bc1be5ade6e199c7501b1e4dff0f))*

### 🐛 Bug Fixes

- **(main)** Incorrect usage of menus *([b610e0f](https://github.com/FlysonBot/Mastermind/commit/b610e0f29b0c8d2debd3eeffc0f213b1e990f68e))*
- **(main)** NumberOfColor is given 2 arguments; Outdated usage of validator *([72ce81a](https://github.com/FlysonBot/Mastermind/commit/72ce81ae85f55150b98479d6a50599c2681a4f7d))*
- **(main)** Validate_input method doesn't return the validated value (which converts the input to appropriate type) *([ab574e2](https://github.com/FlysonBot/Mastermind/commit/ab574e2b7196c4d23b8bdb6cdda2ebb77119ca33))*
- Feedback not displayed *([da49f9f](https://github.com/FlysonBot/Mastermind/commit/da49f9fae85d4ae41cf6dde5b372b146a23bc1c4))*
- Cannot retrieve saved games due to outdated interface *([3fc55c9](https://github.com/FlysonBot/Mastermind/commit/3fc55c91f373c8ef615cfae53cbe89dc8e233d7b))*
- **(main)** Cannot retireve saved game due to incorrect menu handling *([155e663](https://github.com/FlysonBot/Mastermind/commit/155e663178307a424c90797cf4539960d44744b4))*
- **(SavedGameMenu)** Fetch data returned list instead of pandas table *([669423b](https://github.com/FlysonBot/Mastermind/commit/669423b5ded2a6c0d38cb6ec1d597e4a1e8ded1a))*
- Cannot resume game *([14ecdf5](https://github.com/FlysonBot/Mastermind/commit/14ecdf51f42c675ad8b7726a1f98746bb0391e46))*
- **(main)** Cannot display game history *([c654189](https://github.com/FlysonBot/Mastermind/commit/c65418919dcbb853628e965202a88d6e26348345))*
- Error generating game metadata, Game object has no attribute *([36bc1df](https://github.com/FlysonBot/Mastermind/commit/36bc1dfa1e9fec906bce7ce98536c7b6926fcbbc))*
- Missing handling for discarding game *([c4ec2e7](https://github.com/FlysonBot/Mastermind/commit/c4ec2e7e41104f691ab263d05b7143e22fd22f9b))*
- Error creating game with AI solver *([17e2d38](https://github.com/FlysonBot/Mastermind/commit/17e2d38544bb12199ab89d062c002e4647e82429))*

### ⚙️ Miscellaneous Tasks

- Create requirements.txt *([1911d52](https://github.com/FlysonBot/Mastermind/commit/1911d5272c879c6a9a61429eb56bcf7c2cf27acc))*
- Import style fix *([6155bc7](https://github.com/FlysonBot/Mastermind/commit/6155bc78370d2a3f1b6d6fbe036e4410be00ba6b))*
- **(doc)** Improve documentation *([3151983](https://github.com/FlysonBot/Mastermind/commit/31519832820972e7011e33ae62f4b18a89cf3a66))*
- **(docs)** Modify doc generating setting *([1fdee8d](https://github.com/FlysonBot/Mastermind/commit/1fdee8defae681da663869da3711f1bdb58ee38e))*
- **(main)** Remove the menus in main.py and change to use those in  ui/menu *([1e7b978](https://github.com/FlysonBot/Mastermind/commit/1e7b978cacc8a7a84c36da8f3872b555a6bcf1d8))*
- Remove unused User Setting option *([ebe18fd](https://github.com/FlysonBot/Mastermind/commit/ebe18fd5ab608233d90c00769cc50c9531f34d6e))*
- **(menu)** Remove unused import *([b283946](https://github.com/FlysonBot/Mastermind/commit/b283946635df49c76b94c60d161ba86ef16e1676))*
- Create setup.py *([44c9360](https://github.com/FlysonBot/Mastermind/commit/44c9360fee08755a76300aa2f6d27cd8fef82c0c))*
- Update main.rst *([7c26b91](https://github.com/FlysonBot/Mastermind/commit/7c26b919e8a6ad60653f9ca92f956b92ff4a38a0))*

## [v1.5.0-beta](https://github.com/FlysonBot/Mastermind/releases/tag/v1.5.0-beta) - 2024-11-25

More stable pre-release. All modules had been tested throughly and all known bugs fixed. Certain part of the program still not complete or needs further refactoring.

### 🧪 Testing

- **(menu)** Add test for concrete_menus *([fec88f0](https://github.com/FlysonBot/Mastermind/commit/fec88f05b80d530d4bb5b8434e386bb4807e412b))*
- Add additional tests suggested by Sourcery *([87d18e1](https://github.com/FlysonBot/Mastermind/commit/87d18e13cc76d4984d17cf248b38f64b75030b9b))*

## [v1.4.5-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.4.5-alpha) - 2024-11-25

Majority of bugs fixed at this point

### 🐛 Bug Fixes

- **(game)** Method in game_parameter accidently passed self to method of itself *([de88834](https://github.com/FlysonBot/Mastermind/commit/de888343a920b3b947ededac2301ed8ada812936))*
- **(game)** Attempt to check for last guess to determine win status when game had not started *([da1c96f](https://github.com/FlysonBot/Mastermind/commit/da1c96f34b50edad761c5f609618d3d08fbc59e7))*
- **(game)** Game class is missing __len__ method *([f13c539](https://github.com/FlysonBot/Mastermind/commit/f13c5399d3ffdde88e1add7aedc38fc6ed9166c2))*
- **(players)** InputConversionError not excepted in human_player *([c01c5cf](https://github.com/FlysonBot/Mastermind/commit/c01c5cfb5dbb37a3055cd2f52686946ed9801dc0))*
- **(game)** Game is missing the properties that were migrated to GameParameter *([466f7e8](https://github.com/FlysonBot/Mastermind/commit/466f7e898f1e5e7025c669dececfaf9d5bbc3e70))*
- **(players)** External player pass too many parameters to ValidFeedback validation model *([481bc0d](https://github.com/FlysonBot/Mastermind/commit/481bc0d4b463945d7066af95eef0619ab66f3c7f))*
- **(players)** Cannot initialize AICodeCracker with abstract method 'obtain_guess' *([3444a20](https://github.com/FlysonBot/Mastermind/commit/3444a209da54ee05157b855aa0c658110835b788))*
- **(game)** Pass the wrong arugment (instance of Game instead of GameParameter) to PlayerLogic class *([37dd2b2](https://github.com/FlysonBot/Mastermind/commit/37dd2b246ea51d5436d5864e59d4122c6c80dbfd))*
- **(game)** Incorrect reference to self when should actually refer to self.game_state in PlayerLogic *([ef2e82e](https://github.com/FlysonBot/Mastermind/commit/ef2e82e207be20a717a8a45182769f7409c74ebb))*
- **(players)** Pass PlayerLogic instead of Game to players; Modify players to accept PlayerLogic directly to avoid this issue *([ab0ed3f](https://github.com/FlysonBot/Mastermind/commit/ab0ed3fbae9fb2da66a720e91c312482db489b45))*
- **(game)** Incorrect reference to different component *([323601d](https://github.com/FlysonBot/Mastermind/commit/323601da6708cfc3cffc18d4a74c333997d9f0c5))*
- **(game)** Did not return the quit and discard command from code setter *([9db7e58](https://github.com/FlysonBot/Mastermind/commit/9db7e5856ca60c66bc0aec1636ec2daaccebd18a))*
- **(game)** Test for game_flow doesn't run correctly *([d523c26](https://github.com/FlysonBot/Mastermind/commit/d523c26b2997157f2a38d545950fa6d673a4413c))*

### 🚜 Refactor

- **(validation)** Ensure ValidCombination and ValidFeedback raise similar exception types *([3e499fd](https://github.com/FlysonBot/Mastermind/commit/3e499fd8b88fc14ed1f0689cddc5061015131771))*
- **(validation/game_io)** Extract repeated logic of validating integer range in combination and feedback check *([27f1471](https://github.com/FlysonBot/Mastermind/commit/27f147142cc8773a0d068dd55b87dfcc5cc5d06a))*
- **(validation)** Split game_io into 3 files and slightly changes the exception message *([71a23e3](https://github.com/FlysonBot/Mastermind/commit/71a23e32b01fa4b5d64a5a1ecae326cc27c38d4d))*

### 📚 Documentation

- **(validation)** Add missing raises in docstring for validate_combination in ValidCombination *([269568d](https://github.com/FlysonBot/Mastermind/commit/269568d9ce8ee92bcbe4715cd90312e39abe92ee))*

### 🧪 Testing

- **(game)** Add test for board *([99152b2](https://github.com/FlysonBot/Mastermind/commit/99152b2b814dabfcff5b67af0684e25989508e8e))*
- **(game)** Add test for game_parameter *([375c42e](https://github.com/FlysonBot/Mastermind/commit/375c42e9302710fbcce6c5a69661e30e6bf836c2))*
- **(players)** Add test for abstract_player *([6fd0f73](https://github.com/FlysonBot/Mastermind/commit/6fd0f73ca2d35ae5b0a70c81e04f066cd90065e8))*
- **(players)** Add test for human_player *([65c72fb](https://github.com/FlysonBot/Mastermind/commit/65c72fb5bc13539a51fa06698228a47b032926dd))*
- **(players)** Add test for ai_player *([ac3200f](https://github.com/FlysonBot/Mastermind/commit/ac3200fd72c47b48fc0654a5e7c4ad8b7c40376e))*
- **(players)** Add test for external_player *([95ce06c](https://github.com/FlysonBot/Mastermind/commit/95ce06c638cc4ada1f79bdf2bc020bc834030197))*
- **(validation)** Split test for game_io into 3 files (since game_io itself is split) *([7eb7a15](https://github.com/FlysonBot/Mastermind/commit/7eb7a15e958d21a7bdfdd4c66fcd8ffbef9a33ed))*
- **(player)** Add test for player_logic *([95e87a3](https://github.com/FlysonBot/Mastermind/commit/95e87a36ba994609fe0d7477ac434958708b5014))*
- **(players)** Update test to adhere to new changes *([c281be2](https://github.com/FlysonBot/Mastermind/commit/c281be2f9b3531cbbdde1c94179099bac1b07f41))*
- **(game)** Add test for game_flow *([0bbc496](https://github.com/FlysonBot/Mastermind/commit/0bbc496cf05bf6217c1bde840412dc86c62d6660))*
- **(game)** Add test for Game *([3e45e9d](https://github.com/FlysonBot/Mastermind/commit/3e45e9d62fd15d5ac08573e1354726e2089591e3))*
- Add more test to ensrue 100% coverage for players and game package *([ee6a3f5](https://github.com/FlysonBot/Mastermind/commit/ee6a3f5e038bb8aac5cd56bb3a6ac5dd4fceb860))*
- **(game)** Add more test for player_logic to reach 100% test coverage. *([ae56389](https://github.com/FlysonBot/Mastermind/commit/ae56389a23c2376f289def6d0d7ebb161993885d))*

### ⚙️ Miscellaneous Tasks

- **(players)** Update test to adhere to changes elsewhere (exception message / module split) *([3e2cab2](https://github.com/FlysonBot/Mastermind/commit/3e2cab223c62f22b51e4b867a6687a9c5469e8af))*
- **(players)** Update exception handling to ensure uniform behavior as other players *([17431b0](https://github.com/FlysonBot/Mastermind/commit/17431b0a96340d0cbb25c3289179664d92948205))*

## [v1.4.4-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.4.4-alpha) - 2024-11-24

### 🚀 Features

- **(storage)** Add error handling for when file path does not contain a directory component *([05ffc9c](https://github.com/FlysonBot/Mastermind/commit/05ffc9c431e0375b8c3e1eb1f3303ae4b8e1d8db))*

### 🐛 Bug Fixes

- **(menu)** Width calculation did not take into account of the string before the description (key colon and space). *([ad1a3c4](https://github.com/FlysonBot/Mastermind/commit/ad1a3c464d6d88ee071dcc87db9e522985fe99d9))*
- **(menu)** Typo '_empty_message' not '_get_empty_message' *([86c4d61](https://github.com/FlysonBot/Mastermind/commit/86c4d61aec4f5b0949461bbee9f6772fc918ada3))*
- **(storage)** Allow for using different directory and file for user_data *([42ede19](https://github.com/FlysonBot/Mastermind/commit/42ede19bb6a25e36abcf8012d5fdd6bb35ea0ea9))*

### 📚 Documentation

- **(storage)** Clarify the behavior for _modify_item in the docstring *([093b643](https://github.com/FlysonBot/Mastermind/commit/093b643f04420d6127f7e3a631dc7f587cd42148))*

### 🧪 Testing

- **(memu)** Add test for base_menu *([d371fdf](https://github.com/FlysonBot/Mastermind/commit/d371fdf50de4eab536ea8299fd1b4bc43d627480))*
- **(menu)** Add test for option_menu *([b3d57e2](https://github.com/FlysonBot/Mastermind/commit/b3d57e2dd4b8fd74753a14f558197d80fec22c51))*
- **(menu)** Add test for data_menu *([a9be228](https://github.com/FlysonBot/Mastermind/commit/a9be22837d1865d8d2177d6e11ac0cc69f2dba82))*
- **(utils)** Add white peg test for get_feedback *([55570bd](https://github.com/FlysonBot/Mastermind/commit/55570bd5e7a3a799d9f03dcf41657178a65637e7))*
- **(utils)** Update f-string test to test edge cases *([b58c4e7](https://github.com/FlysonBot/Mastermind/commit/b58c4e75dfe2d8c91d1cb1726fae2e06243ef58d))*
- **(storage)** Add test for persistent cache *([1b3e16f](https://github.com/FlysonBot/Mastermind/commit/1b3e16f0e763fef1a25161d6be2c3ab7b42c8d19))*
- **(storage)** Add test for user_data *([2233c6b](https://github.com/FlysonBot/Mastermind/commit/2233c6bf32ce8bdb4ffddd70ab30fb89f63119eb))*
- **(storage)** Add testing for corrupted pickle data *([edda3c4](https://github.com/FlysonBot/Mastermind/commit/edda3c45a475e2980801d1aed03dde7d8c8337e0))*
- **(storage)** Test that persistance cache persist between multiple instances. *([677116f](https://github.com/FlysonBot/Mastermind/commit/677116f8fd4528a78b57c8a3b153bfddbf5b5b53))*

### ⚙️ Miscellaneous Tasks

- **(storage/user_data)** Use name assignment to simplify expression *([c5a900f](https://github.com/FlysonBot/Mastermind/commit/c5a900f3b1d361111e5d3135e9f2614a1bc364ba))*

## [v1.4.3-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.4.3-alpha) - 2024-11-24

### 🧪 Testing

- **(utils)** Add test for f-string template *([7dfb33e](https://github.com/FlysonBot/Mastermind/commit/7dfb33ef68cbda5561e0b8fb3fafc851956456e6))*
- **(utils)** Add test for get_feedback *([3fb6424](https://github.com/FlysonBot/Mastermind/commit/3fb64241d43699317ad3cc0b9d3d853e9d5a2e85))*
- **(utils)** Add test for render_dataframe *([c8d25a7](https://github.com/FlysonBot/Mastermind/commit/c8d25a7bffc4aa5e672236dd128b2b11a2bc30ea))*
- **(utils)** Add test for stack *([1b07791](https://github.com/FlysonBot/Mastermind/commit/1b07791058d7902fa505b1ee66bcb7259987fa0a))*

## [v1.4.2-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.4.2-alpha) - 2024-11-24

### 🐛 Bug Fixes

- **(validation/semi_mutable)** Method validate_modifications does not return a value *([b37bb77](https://github.com/FlysonBot/Mastermind/commit/b37bb777ffb232bb9c07d5390694f8eff131b8d5))*
- **(vscode)** Workspace folder is not in Python Path *([6769deb](https://github.com/FlysonBot/Mastermind/commit/6769deba24a5cffa8cd5c0291059202d43f1cc7f))*
- **(validation/game_io)** Did not catch error of too large of feedback sum; Check for the wrong thing for validate_arguments *([bef6e9d](https://github.com/FlysonBot/Mastermind/commit/bef6e9d28b3531232a3e0a3c323fb4411814f753))*

### 🧪 Testing

- **(validation/semi_mutable)** Add test *([fbc620e](https://github.com/FlysonBot/Mastermind/commit/fbc620eb583bd382c7106d059d5cc27d87118751))*
- **(validation/ValidatedClass)** Add test *([e785b1a](https://github.com/FlysonBot/Mastermind/commit/e785b1aa6218d2b24c2eb00f7564683707a81759))*
- **(validation/model/numeric)** Add test *([cc784c1](https://github.com/FlysonBot/Mastermind/commit/cc784c1f0258bb6d21e0136ea68b18d744a516bc))*
- **(validation/game_io)** Add test *([767b57e](https://github.com/FlysonBot/Mastermind/commit/767b57ef33af64e216943b427618ddf1764ad4fa))*

## [v1.4.1-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.4.1-alpha) - 2024-11-24

### 🚀 Features

- **(game)** Use ValidatedClass in game_parameter *([adc7f30](https://github.com/FlysonBot/Mastermind/commit/adc7f306891ba95eab89a8ea0811ea23f85ab2bf))*
- **(validation)** Raise RangeError instead of ValueError when number in combination is out of acceptable range *([c896001](https://github.com/FlysonBot/Mastermind/commit/c896001368d6aedf94a61de11146ff1e1bb63758))*

### 🐛 Bug Fixes

- **(validation)** NumberRangeModel is not a generic class *([7266941](https://github.com/FlysonBot/Mastermind/commit/7266941ab3acc97b8002d2ecb06df6fb356457a3))*
- **(validation)** Missing import in __init__.py *([9044cd2](https://github.com/FlysonBot/Mastermind/commit/9044cd236243d8b29c3a6a36b162d76858c14f2e))*
- **(game)** Reference to removed classes; replaced with new classes *([af90925](https://github.com/FlysonBot/Mastermind/commit/af909258c8008ca2395d0a932dca0a2c7275809a))*
- **(players)** Circular import of "Game" class *([437fcfa](https://github.com/FlysonBot/Mastermind/commit/437fcfae2616b14c3254a456c8b24849168e2262))*
- **(players)** Remove use of deleted BaseModel class *([3d50fc1](https://github.com/FlysonBot/Mastermind/commit/3d50fc1b612a4a1b96fe3943e3377e7cd19affc1))*
- **(game)** Replace deleted ValidatedData with the new Validator *([c0b0bab](https://github.com/FlysonBot/Mastermind/commit/c0b0bab6d9da76b40ab2c750292bd9d82b904d4e))*
- **(validation)** Missing import for Validator *([474eba7](https://github.com/FlysonBot/Mastermind/commit/474eba7db328d306bcf66f3cbe5d336274e0f578))*
- **(validation)** When only one of the 4 constrain for NumberRangeModel is used, comparing maximum and minimum range lead to comparison with NoneType *([9a9e4bc](https://github.com/FlysonBot/Mastermind/commit/9a9e4bca8f86d97824e650311ae75cf92defbfea))*
- **(validation)** 'If x statement' also return False for zeros, replace with 'If x is not None' *([183f224](https://github.com/FlysonBot/Mastermind/commit/183f2240984764009dd82421ff9eaca9f0df7a7b))*

### 🚜 Refactor

- **(game)** Remove unnecessary use of validation module *([b9a1d2b](https://github.com/FlysonBot/Mastermind/commit/b9a1d2b1b64b21b2f499d8281b58d5e48fac3b1b))*

### 🧪 Testing

- **(validation)** Add more tests *([f436d9a](https://github.com/FlysonBot/Mastermind/commit/f436d9a4e3b71ccf5b8ea6b68f045d1c2278a676))*

### ⚙️ Miscellaneous Tasks

- **(players)** Update to use ValidCombination instead of the old ValidGuess, and except the specific custom exceptions *([5c5f552](https://github.com/FlysonBot/Mastermind/commit/5c5f5529caec5bd23dad473fa0ecd58df4468925))*
- **(vscode)** Update test file directory path *([11aa812](https://github.com/FlysonBot/Mastermind/commit/11aa812fc1d0b5341f7b2f07fa0fa502699dd7fe))*

## [v1.4.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.4.0-alpha) - 2024-11-23

### 🚀 Features

- **(docs)** Initialize Sphinx for documentation *([1c76986](https://github.com/FlysonBot/Mastermind/commit/1c7698645718dc5830f936b58f319589a912393c))*
- **(docs)** Set up documentation *([931c0bc](https://github.com/FlysonBot/Mastermind/commit/931c0bc454571a9989303bf2258038d1a8449d64))*

### 🐛 Bug Fixes

- **(utils)** Missing __all__ in __init__.py *([0d3eb6a](https://github.com/FlysonBot/Mastermind/commit/0d3eb6a237e6f46ceaba60d0f38d7e604c6c13f7))*

### 🧪 Testing

- Create new tests folder and one test file per code file *([14aecf0](https://github.com/FlysonBot/Mastermind/commit/14aecf02cdf76cee58ccf23e500979d44dde86e5))*
- Add __init__.py in test packages *([6649b67](https://github.com/FlysonBot/Mastermind/commit/6649b67f6e020fea6cbcc77b15576cca19575f0c))*
- **(validation)** Add test for base *([feb82e4](https://github.com/FlysonBot/Mastermind/commit/feb82e42ac7ea74bea134f52f66bbb35570db545))*

### ⚙️ Miscellaneous Tasks

- **(test)** Remove old tests *([a48f8f5](https://github.com/FlysonBot/Mastermind/commit/a48f8f52aae51129157ab19a07184f144c3ef3ec))*

## [v1.3.1-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.3.1-alpha) - 2024-11-22

### 🐛 Bug Fixes

- **(game)** Change game_state to game_parameter to reflect the changed class name *([40bb894](https://github.com/FlysonBot/Mastermind/commit/40bb894d698ae0de2aeb8268ed3f199fc8815dcd))*

### 📚 Documentation

- **(game)** Add comprehensive docstring and improve code documentation *([54bf87f](https://github.com/FlysonBot/Mastermind/commit/54bf87f2c46f9b7d77b825b9bdaf9f82df7272a2))*
- **(storage)** Add docstring *([1c5b2e0](https://github.com/FlysonBot/Mastermind/commit/1c5b2e01ecaa59c6f8ba88f36edd4d85ac0e33aa))*
- **(menu)** Add docstring *([196c355](https://github.com/FlysonBot/Mastermind/commit/196c3552207d5176745231b71edaec7cdff2f1f9))*
- **(utils)** Add docstring *([c05d23f](https://github.com/FlysonBot/Mastermind/commit/c05d23fe98d62abaf6a67d17321a846013e9c485))*
- **(validation)** Add docstring *([d1e02a6](https://github.com/FlysonBot/Mastermind/commit/d1e02a63bbe0af92ed2f215f0e5230959c96bf86))*
- Improve docstring *([ea3ce1c](https://github.com/FlysonBot/Mastermind/commit/ea3ce1c4f77836ec23282e3f8d0037e3deb0751b))*

### 🎨 Styling

- **(game)** Expand single-line docstring to 3 lines for readability *([5cd4813](https://github.com/FlysonBot/Mastermind/commit/5cd4813d05d95fc8fe982f99eac9688afddb04d7))*

## [v1.3.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.3.0-alpha) - 2024-11-22

### 🐛 Bug Fixes

- **(validation)** Exceptions not imported in validation subpackage *([445093c](https://github.com/FlysonBot/Mastermind/commit/445093c59de0bc50efd2622ae0c77d8a1fab0daf))*
- **(game)** Missing parameters for GameState and repeated creation of GameBoard *([52ee77d](https://github.com/FlysonBot/Mastermind/commit/52ee77d2f1ff32c69ab2b2244cfea6936def9429))*
- **(player)** CodeSetter and CodeCracker were not set as abstract classes *([a3b3fe6](https://github.com/FlysonBot/Mastermind/commit/a3b3fe630697f36e05f7b4134400a5409f13371b))*

### 🚜 Refactor

- **(game)** Simplify player initialization and game logic *([6ef5afc](https://github.com/FlysonBot/Mastermind/commit/6ef5afc224c746a87a011b921480c8b5dd71adb1))*
- **(game)** Move result output logic to game flow *([bde91d5](https://github.com/FlysonBot/Mastermind/commit/bde91d56ab682a48f7a1a68d98efb3a5578898dd))*

### 🎨 Styling

- Improve readability by adding new lines *([848cb4d](https://github.com/FlysonBot/Mastermind/commit/848cb4d89e3337fc6b9ee3d8ee41b766e25f549d))*
- Remove all existing docstring for easier code modification *([befac39](https://github.com/FlysonBot/Mastermind/commit/befac39d16fe546409f6c1bd06ea47663a0d25a3))*

## [v1.2.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.2.0-alpha) - 2024-11-21

### 🚀 Features

- Add __all__ attribute to all __init__.py *([f64ce63](https://github.com/FlysonBot/Mastermind/commit/f64ce632ed70604d0a59eea8bb16cf611c6281a2))*

### 🚜 Refactor

- Improve code structure, size, working memory, and minor optimization *([1d5a501](https://github.com/FlysonBot/Mastermind/commit/1d5a50114dda8c9fe26cc6608908f76dc2978854))*
- Rename classes and methods for improved clarity and consistency *([ce15aa8](https://github.com/FlysonBot/Mastermind/commit/ce15aa80f289e857718f8f3e75201fd9b2f793e5))*
- **(game)** Restructure game logic into separate components *([3013a07](https://github.com/FlysonBot/Mastermind/commit/3013a0748e6961e8dfd80b9cbb3f00777ded8bb0))*

### 🎨 Styling

- Format with ruff *([b5b92a1](https://github.com/FlysonBot/Mastermind/commit/b5b92a1f6b9345444f68a6c6cb2fa037f2fa0f5b))*

### ⚙️ Miscellaneous Tasks

- Remove unnecessary extension recommendation and add ruff *([db604f5](https://github.com/FlysonBot/Mastermind/commit/db604f59012ead441a735269095e5e77bbb09eb8))*

## [v1.1.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.1.0-alpha) - 2024-11-20

Split all the modules package(s) with smaller modules.

### 🐛 Bug Fixes

- Stack.py missing import statements *([7b8095c](https://github.com/FlysonBot/Mastermind/commit/7b8095cd30b00456aeb89dd4046ca08c5cf15c43))*
- No module name 'src' *([8b67981](https://github.com/FlysonBot/Mastermind/commit/8b67981e0edd3135ae2ef5ca04d9213baa6c2c5c))*

### 🚜 Refactor

- **(menu)** Extract abstract base class and split into 4 files *([46b527c](https://github.com/FlysonBot/Mastermind/commit/46b527c1054ff52888761f553ccc5f7f92d0f132))*
- **(validation)** Split and organize validation folder, improve modularity *([f832978](https://github.com/FlysonBot/Mastermind/commit/f83297821fb4543526d7f113a7c61458d729a6a4))*

## [v1.0.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v1.0.0-alpha) - 2024-11-18

Restructured the entire repo.

### 🐛 Bug Fixes

- **(test)** Tests not discovered *([5eb1764](https://github.com/FlysonBot/Mastermind/commit/5eb1764c86642549adfdc86e0396b8dd4fb22fe0))*
- No modules name 'players', 'game', etc. *([71d2f51](https://github.com/FlysonBot/Mastermind/commit/71d2f5186dd1bdbbaa70093108e562ea15ab9622))*
- **(test)** Cannot import main *([50d10fb](https://github.com/FlysonBot/Mastermind/commit/50d10fbe98b913bd320ae5ffee071e5db329e46d))*

### 🚜 Refactor

- **(storage)** Split storage_handler into 2 *([8eb0de3](https://github.com/FlysonBot/Mastermind/commit/8eb0de372f2a4fd5623863a589684d7e2ada3f84))*
- **(player)** Split into 4 files *([9b986f0](https://github.com/FlysonBot/Mastermind/commit/9b986f0490e2ceecef6a8cc97e036bf45b34ad12))*
- **(utils)** Split utils into 4 files *([2a1d4ed](https://github.com/FlysonBot/Mastermind/commit/2a1d4ed81158d7d5d601bb2415b90b7e1c336843))*
- **(game)** Split into 2 files *([e72ff6e](https://github.com/FlysonBot/Mastermind/commit/e72ff6edbebe42c642bff5146e36cae08c093501))*
- **(import)** Change import in __init__.py to absolute import *([62d129e](https://github.com/FlysonBot/Mastermind/commit/62d129e7cb23f749d8ddea0705cdd06ec1773b3c))*
- **(import)** Shorten import statement when importing other packages *([7aff440](https://github.com/FlysonBot/Mastermind/commit/7aff4408d79290d61160f6e131c5a1a8d0feb537))*

### ⚙️ Miscellaneous Tasks

- Change testing directory *([a6daab7](https://github.com/FlysonBot/Mastermind/commit/a6daab7516e64c29849cc32593a11f9dd0aa4375))*

## [v0.5.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v0.5.0-alpha) - 2024-11-17

### 🚀 Features

- **(main)** Add game to history if game is not done *([b2c0a17](https://github.com/FlysonBot/Mastermind/commit/b2c0a17da6e5d9e0ea899b2831c9a7b7b52bd874))*
- **(utils)** Print pandas dataframe in plain text align to the left *([3c27e1f](https://github.com/FlysonBot/Mastermind/commit/3c27e1fa4de4f6013d55b243ede032ce6e994ccc))*
- **(utils)** Render_dataframe can now render index column *([518bc7c](https://github.com/FlysonBot/Mastermind/commit/518bc7cafd5913f5d9200b8a9792f24cbf2987f1))*
- **(main)** Allow resume game, menu allow custom return key and add menu width *([f3f0873](https://github.com/FlysonBot/Mastermind/commit/f3f0873b8e3347fc9f344f991e830a0f2f905526))*
- **(storage)** Add bracket notation support *([7372a3e](https://github.com/FlysonBot/Mastermind/commit/7372a3ec91d97dbb458b61fd3c73cf7957a630f6))*

### 🐛 Bug Fixes

- **(test)** Mastermind module not found *([efd26cc](https://github.com/FlysonBot/Mastermind/commit/efd26cc12efb15dda7f643d0f9b00a98c64f192d))*
- **(main)** _Board type have no attribute _guesses *([45a4bbc](https://github.com/FlysonBot/Mastermind/commit/45a4bbc4b43900f52cfdbc781ccc28a2d6f98062))*
- **(main)** Game history doesn't work *([5650ec5](https://github.com/FlysonBot/Mastermind/commit/5650ec5646c96fe7c38ad0c6e0b2261655f65c2a))*
- **(test storage)** Test for clear all doesn't work when there already exists a config file *([f5d99f8](https://github.com/FlysonBot/Mastermind/commit/f5d99f8cbf7ee690e3c78bd0ac5326300fe81a63))*
- **(player)** Secret_code not found *([d125534](https://github.com/FlysonBot/Mastermind/commit/d125534fe7488bdc18fb988df382fd03037cdc6f))*

### 🚜 Refactor

- **(main)** Game history display format *([b8b6558](https://github.com/FlysonBot/Mastermind/commit/b8b65586980a98972b58bf56e03d285355319bf8))*

### ⚙️ Miscellaneous Tasks

- Exclude data folder *([85f02e6](https://github.com/FlysonBot/Mastermind/commit/85f02e6bdb2d35ce294d51e6f425d1977b0b1051))*

## [v0.4.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v0.4.0-alpha) - 2024-11-17

### 🚀 Features

- **(storage)** Allow checking if a key exist in UserData *([a9a9110](https://github.com/FlysonBot/Mastermind/commit/a9a9110ff07a2ee3cb648d58fe1392069fd72477))*
- **(main)** Add feature to save game *([6676085](https://github.com/FlysonBot/Mastermind/commit/66760859f79f813a78fd72df2cdcb975c0f33d0e))*
- **(main)** Replace game statistic with game history, allow menu without options (replace with other logic) *([87e4e27](https://github.com/FlysonBot/Mastermind/commit/87e4e271fb46869b69ac1a4a5179b1483628d998))*

## [v0.3.2-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v0.3.2-alpha) - 2024-11-17

### 🚜 Refactor

- Change folder name from mastermind to main *([51ad48a](https://github.com/FlysonBot/Mastermind/commit/51ad48af8938ff58c565785e8ed9e22bb4340cc5))*

### 📚 Documentation

- Improved docstring for important class and methods *([d2e19d5](https://github.com/FlysonBot/Mastermind/commit/d2e19d5dfb5633a962c01622bff1f5052b9be3dc))*
- **(main)** Improved docstrings in main.py *([05dccf7](https://github.com/FlysonBot/Mastermind/commit/05dccf7e27f2dcc94537c82e520f094e22ed46d6))*
- **(storage)** Improved documentatoin *([55235e2](https://github.com/FlysonBot/Mastermind/commit/55235e2dced26f262734d05a588de696e3685d0b))*

## [v0.3.1-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v0.3.1-alpha) - 2024-11-17

### 🚀 Features

- Update gitignore to push vscode settings to repo to allow workspace consistency when cloning *([f385bca](https://github.com/FlysonBot/Mastermind/commit/f385bca1583f530655f303ab2efa7d66f4f2a590))*
- **(vscode)** Update setting.json to use isort and black *([1e4e79d](https://github.com/FlysonBot/Mastermind/commit/1e4e79d1978a261dcef6022028b65e842c7b7b6b))*
- **(vscode)** Add python test adapter extension *([203379e](https://github.com/FlysonBot/Mastermind/commit/203379e9cc1c0f622b824375dea0632499154fdc))*
- **(vscode)** Add vscode action button extension *([9edfe07](https://github.com/FlysonBot/Mastermind/commit/9edfe07cd08042cd759adf9ebc1a609ef47a78c5))*
- **(vscode)** Add launch.json for debugger *([5d105f7](https://github.com/FlysonBot/Mastermind/commit/5d105f7ae25a3f16730cf3c0b408888cb45ba518))*

### 🐛 Bug Fixes

- Change ValidationError to ValidatedData.ValidationError *([ec3588b](https://github.com/FlysonBot/Mastermind/commit/ec3588b4fac60a7f6d1093ce07e795062a3d23a2))*
- **(vscode)** Remove unnecessary flutter extension *([1fad991](https://github.com/FlysonBot/Mastermind/commit/1fad9910273decdd09de2afea10c9f953d81d3e5))*
- **(vscode)** Remove auto docstring extension *([af08e49](https://github.com/FlysonBot/Mastermind/commit/af08e4965362e2da3c846b5036152acfa8fa848e))*

### 🚜 Refactor

- Move all packages into a newly created src folder *([ee1b1c5](https://github.com/FlysonBot/Mastermind/commit/ee1b1c59ec3828c0ec502502d9d71a20cad1bbda))*
- Move main.py and test.py into src folder *([3020acd](https://github.com/FlysonBot/Mastermind/commit/3020acdb8d670bae5727f12051b9650ad8c1e101))*
- Apply Sourcey suggestion and change style *([876fb0b](https://github.com/FlysonBot/Mastermind/commit/876fb0bc9f1c3f2cc3792821f1bad8985c69f54c))*
- **(main)** Raise more specific error and remove else after guard condition *([0179209](https://github.com/FlysonBot/Mastermind/commit/01792099d881e74e296db9b2732616a844a419dd))*

### 🎨 Styling

- Fix spelling *([a6b84d0](https://github.com/FlysonBot/Mastermind/commit/a6b84d03ad05e7ace95409be77bb2408d6b7105e))*
- Only include necessary import and avoid import all *([8c1db24](https://github.com/FlysonBot/Mastermind/commit/8c1db242d9b46de09981462aa6ea60f6b7926d9b))*

### ⚙️ Miscellaneous Tasks

- Update gitignore to include .vscode/ *([d5c6ee2](https://github.com/FlysonBot/Mastermind/commit/d5c6ee26aaf40a9ebf6aae098bb71a5e226ec44f))*
- Update gitignore to exclude test coverage file *([f535052](https://github.com/FlysonBot/Mastermind/commit/f5350521a185f608e4d7c234e423e27c3da12ccb))*
- **(vscode)** Change true to explicit *([b7ff6b2](https://github.com/FlysonBot/Mastermind/commit/b7ff6b2c6df4e11a6dc17abf4e8b511238a637d2))*

## [v0.3.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v0.3.0-alpha) - 2024-11-11

### 🚀 Features

- Update storage_handler to use pickle to support serialization of instance of custom class *([13a954b](https://github.com/FlysonBot/Mastermind/commit/13a954b5113ad0cde7f4abc54fcb24d74ee1b403))*
- Add .gitignore *([6a215ad](https://github.com/FlysonBot/Mastermind/commit/6a215ad8e9d5a4dabf52e338b5e0e7bc2c866f5f))*

### 🐛 Bug Fixes

- **(main)** Typo; update with MainUI class *([2550b06](https://github.com/FlysonBot/Mastermind/commit/2550b06c6fb3f9ef62d5e09368b86234b5c85661))*
- **(main)** Cannot instantialize Menu subclass and start_new_game missing parameters cls *([69ec428](https://github.com/FlysonBot/Mastermind/commit/69ec428f70404c6483126f4e810a2b381fc6f732))*

### 🎨 Styling

- Apply Black style *([9c5e550](https://github.com/FlysonBot/Mastermind/commit/9c5e5502ce6797330a9ecb543e542cd32d38bc22))*

## [v0.2.2-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v0.2.2-alpha) - 2024-11-11

### 🐛 Bug Fixes

- Relocate test.py and change to a simpler logic *([0f5fee0](https://github.com/FlysonBot/Mastermind/commit/0f5fee0a3fe547f990eda634d352e7fc4972d8ec))*
- Add project root directory to sys.path in test.py *([f4a6f12](https://github.com/FlysonBot/Mastermind/commit/f4a6f124f6c53620b3daa5b444f4a7da58cf7bf5))*
- Gameboard test initialize player before submit guess *([80092df](https://github.com/FlysonBot/Mastermind/commit/80092df9cdf379f554aa376f04f33f8b94b9824c))*
- **(storage)** Custom set and get attribute method not called; change class to singleton *([28a0bfe](https://github.com/FlysonBot/Mastermind/commit/28a0bfe6f5e6540147e3d7c71f2a95439e3dd2d6))*
- Change other reference to UserData to adhere to singleton class invocation *([f17ee7b](https://github.com/FlysonBot/Mastermind/commit/f17ee7bc23b01d4364c573e7c72e2ca48cdf20e6))*
- SecretCode not found; change to ValidGuess *([b065517](https://github.com/FlysonBot/Mastermind/commit/b065517391125a45b1c9f1ec6107116be2787a0a))*
- **(test_players)** No module named 'players'; change patch from players.getpass to getpass.getpass *([9e20043](https://github.com/FlysonBot/Mastermind/commit/9e200436466f54d1f83fd0b1e279d3fbda200432))*
- **(test_players)** Module 'players' not found; change patch from 'players' to 'mastermind.players' *([bff803e](https://github.com/FlysonBot/Mastermind/commit/bff803eae8796d4c37d76eb4ea8ef2388c48e0b0))*

### 🚜 Refactor

- Move main.py and test.py outside of package into the parent directory *([71e6dbf](https://github.com/FlysonBot/Mastermind/commit/71e6dbf43f7bc2a02200b904ccf397f880f6ac20))*
- Revert back to simple test discovery *([f2f9418](https://github.com/FlysonBot/Mastermind/commit/f2f9418141e2f8c7b9233c7a1a5d35bb4036b522))*
- **(test_players)** Import getpass directly *([d930278](https://github.com/FlysonBot/Mastermind/commit/d93027819ea9e2ccb8fb03468494690f76948d59))*
- **(test_players)** Return back *([d29b968](https://github.com/FlysonBot/Mastermind/commit/d29b96821ed7608b84eb91784e10ff6c36c3a713))*

### 📚 Documentation

- Remove comments for import statements *([677a714](https://github.com/FlysonBot/Mastermind/commit/677a714e01240781efc5ff2bef84e0e512750e49))*
- Remove comments for import statements (continue) *([7f915a9](https://github.com/FlysonBot/Mastermind/commit/7f915a9e2e2e4ce77209d730a844a0a1f30458c0))*

## [v0.2.1-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v0.2.1-alpha) - 2024-11-10

### 🐛 Bug Fixes

- Missing import and typo in gameboard *([78f2e46](https://github.com/FlysonBot/Mastermind/commit/78f2e46c6653bb3d789b2fa726ac0d7eec34012b))*
- Type hint of not imported class in players *([5d2ef59](https://github.com/FlysonBot/Mastermind/commit/5d2ef5939e31f78bb2a9d3193f4b5d4204b27656))*
- Move stack to utils to avoid circular import *([2879374](https://github.com/FlysonBot/Mastermind/commit/28793744c51723c2f4a435db39b8966dec43e1ba))*
- Optinal is not defined *([e4fc284](https://github.com/FlysonBot/Mastermind/commit/e4fc28495f605469ca9d935b8019f69a2e29b806))*
- Utils missing import for Stack *([b93be87](https://github.com/FlysonBot/Mastermind/commit/b93be8778b2c56b6381cef2d54723e411dce24dc))*
- Unnecessary abstract method obtain_guess in ABC class Player *([b455c5f](https://github.com/FlysonBot/Mastermind/commit/b455c5fff321ae6bbbe4e420ead2d5e32973fe19))*
- ConstrainedInteger not defined typo in validation *([c88600c](https://github.com/FlysonBot/Mastermind/commit/c88600ceb8ddcd2c8a830e6d26cfdf04c79ac3e2))*
- Rename PLAYER1 and PLAYER2 to fix and avoid naming mismatch *([778ea0d](https://github.com/FlysonBot/Mastermind/commit/778ea0d2fa0ad167e1f5fdb522c44806fe48a71b))*
- Player naming issue continue in gameboard *([801d99d](https://github.com/FlysonBot/Mastermind/commit/801d99da96c88b52a0b547e7b4f887a946374a51))*
- Expected quit and discard command not returned *([c4a3cd7](https://github.com/FlysonBot/Mastermind/commit/c4a3cd7c479f383de850a93decc7863887de70e0))*
- Utils func 'get_feedback' rely on 'self' *([e8cf855](https://github.com/FlysonBot/Mastermind/commit/e8cf855e84d898512a8569e7de9545cfa2b1d796))*
- Name conflict for 'win_message' and 'lose_message' *([387f583](https://github.com/FlysonBot/Mastermind/commit/387f583fe718ff0b60c21ecbc4181eaaee83d29f))*
- Return actual feedback instead of ValidFeedback *([908f364](https://github.com/FlysonBot/Mastermind/commit/908f364125344ef9d90a8f3b9f18dfe1ac16a014))*
- Add exception handling for ValidationError when obtaining guess or feedback *([75390f5](https://github.com/FlysonBot/Mastermind/commit/75390f586675f7b27b845742acb3fef8a3d37246))*
- ValidGuess.validate() doesn't return a value *([b57f45b](https://github.com/FlysonBot/Mastermind/commit/b57f45b4165945d049681f790510e55fbc6969cb))*
- Incorrect parameter passed to FStringTemplate.eval() when printing win and lose message *([15b3eed](https://github.com/FlysonBot/Mastermind/commit/15b3eed4dcdf4ea9a0a06708eede09f290c99de2))*
- Remove typo period at the end of players.py *([3f137b0](https://github.com/FlysonBot/Mastermind/commit/3f137b0a49385837ecf5df5feb47230397fd7286))*
- Make undo method abstract to allow subclass to decide what to undo *([1a5d766](https://github.com/FlysonBot/Mastermind/commit/1a5d7667d996359ddbe37dc468e56e724162e000))*
- Stack not cleared after new guess *([2ee1eda](https://github.com/FlysonBot/Mastermind/commit/2ee1eda1f9321b047a174779b8baab7158126bad))*
- Test.py doesn't run when working directory is not at the package *([971fa1c](https://github.com/FlysonBot/Mastermind/commit/971fa1c0eb660feedfd892e4dbec2ec707c66102))*

### 💼 Other

- Apply Black style on main.py *([d8002e0](https://github.com/FlysonBot/Mastermind/commit/d8002e0d39dfb2301adae3f47c9a8a9fb5ac63dc))*

### 🎨 Styling

- Apply Black style *([cf6badd](https://github.com/FlysonBot/Mastermind/commit/cf6badd5fac4a406ff795a2f08edef5a6f17cf93))*

### 🧪 Testing

- Add test for gameboard *([c3cfc86](https://github.com/FlysonBot/Mastermind/commit/c3cfc869ec24abedde24d9d410ba4562b6ff9c5a))*
- Add test for players *([99728ba](https://github.com/FlysonBot/Mastermind/commit/99728ba9aadab931f5ecfa414af0be0ad0c4dff1))*
- Add test for undo and redo functionality *([32e1b01](https://github.com/FlysonBot/Mastermind/commit/32e1b018bcbb447ab7b56072459ca40b943dc2bf))*
- Add test for stack clear after new guess *([f76ef29](https://github.com/FlysonBot/Mastermind/commit/f76ef29307c5315404d8bb7f17f00e31a7581d29))*
- Add a test.py that run all the tests in the tests directory *([5274cb4](https://github.com/FlysonBot/Mastermind/commit/5274cb4ebdc7623255d260358cb965c13a138ced))*

## [v0.2.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v0.2.0-alpha) - 2024-11-10

### 🚀 Features

- Complete MainUI logic; add GameHandler; rename save_data method *([8b9f405](https://github.com/FlysonBot/Mastermind/commit/8b9f40562c689c8bbaed0aac3cae928153600bca))*

### 🚜 Refactor

- Divide GameSimulator into multiple classes to enforce single-responsibility-principle *([0fd5fe4](https://github.com/FlysonBot/Mastermind/commit/0fd5fe428bf0dbc56670c51e765df71f0d46ba9d))*

### 🎨 Styling

- Apply Black fomatter to adhere to PEP8 style, with line max length 88 chars per Black's suggestion *([a5c7a75](https://github.com/FlysonBot/Mastermind/commit/a5c7a75eab4d48165c7e8ef8e14760cef1adeec0))*
- Apply isort style to import statements *([ae543bc](https://github.com/FlysonBot/Mastermind/commit/ae543bcbea470700501840d90a834728e9d67518))*
- Add type hint for main.py *([897ab77](https://github.com/FlysonBot/Mastermind/commit/897ab77428f1ca3684669146d92763f65ccda71b))*
- Remove type hint at definition of variable *([9084e87](https://github.com/FlysonBot/Mastermind/commit/9084e8752bae51f3c5cd342d167561b445a44d26))*
- Ai-refactor style to improve readability and comprehension *([84dd583](https://github.com/FlysonBot/Mastermind/commit/84dd583e14d04d3d91a90a0f83a605d8f0148f5c))*

## [v0.1.0-alpha](https://github.com/FlysonBot/Mastermind/releases/tag/v0.1.0-alpha) - 2024-11-09

Initial pre-release. Entry point defined but incomplete; core functionality scripts included but untested.

### 🚀 Features

- Colab intergration attempt *([4224a66](https://github.com/FlysonBot/Mastermind/commit/4224a66fbc38890c01341f903e6c7cd28a3dd2e1))*
- Automatically apply validation models *([a45ddb5](https://github.com/FlysonBot/Mastermind/commit/a45ddb54d63adbe6047eb20811fbe4ca69793d3c))*
- Allow validation chaining *([ea6cd29](https://github.com/FlysonBot/Mastermind/commit/ea6cd29d4fe5db832d7ee58389b5d71e30ee120f))*
- Automatically convert user input to desired type *([0f4c3b6](https://github.com/FlysonBot/Mastermind/commit/0f4c3b6f9f75cf63b1b3b0d690aad1d8d6b5c0c1))*
- Add more validated types *([1714ac7](https://github.com/FlysonBot/Mastermind/commit/1714ac7cd84e6e74b8e0231c4f215a80389d4173))*
- Allow additional parameters for more advance validation *([cfcf190](https://github.com/FlysonBot/Mastermind/commit/cfcf190eb7a1bf3fa614cee742f74d7254aac0aa))*
- Add more validated types *([1f9f4f2](https://github.com/FlysonBot/Mastermind/commit/1f9f4f20fea289ec6c3957317f71eb04b3693a85))*
- Add support for confined integer *([7edf866](https://github.com/FlysonBot/Mastermind/commit/7edf866ed05a7566f01a4e1907dc583fb1c71e6b))*
- Implement stack with collections.deque *([9207e2d](https://github.com/FlysonBot/Mastermind/commit/9207e2d5cc95160ca326b8e24e9cb3f2e6d1bdf4))*
- Add board class to manage game board status *([93e594f](https://github.com/FlysonBot/Mastermind/commit/93e594f44cc6173735c02752857626c83d2c23bf))*
- Add game logic on top of board to allow player to play game *([29501c1](https://github.com/FlysonBot/Mastermind/commit/29501c180fca5846e6c133425306d967a6dd7a18))*
- Define basic player interaction interface *([3cd2f3b](https://github.com/FlysonBot/Mastermind/commit/3cd2f3b0c9385c2ffd16938b7b83db2ff80c8958))*
- Allow resume game that had started *([0d47662](https://github.com/FlysonBot/Mastermind/commit/0d47662d3eeab73d1010080b6fdd07196f7c717e))*
- F-string template utlity *([5fa714b](https://github.com/FlysonBot/Mastermind/commit/5fa714bd6c644cd4edd63bd0d3b0badc7d0eecd4))*
- ValidGuess support string conversion *([a737f5b](https://github.com/FlysonBot/Mastermind/commit/a737f5b20a4b26ea67d3cfa88d9f465ad3812d28))*
- ValidFeedback support string conversion *([5a3d414](https://github.com/FlysonBot/Mastermind/commit/5a3d4143c1986d026a1433ba3cc12f1074067338))*
- ValidGuess support comma separated string conversion *([6aff68b](https://github.com/FlysonBot/Mastermind/commit/6aff68b3b16d58b3a70522114cb40cac76abb551))*
- Implement human player basic interaction *([2bada8e](https://github.com/FlysonBot/Mastermind/commit/2bada8e1538aed47aca236c7a3f1509438435900))*
- Implement AISetter and ExternalSetter class *([47370dd](https://github.com/FlysonBot/Mastermind/commit/47370dd058e9ff40023980fbf12c81d3b1119219))*
- Intercept discard, quit, undo, and redo command *([fe1a36c](https://github.com/FlysonBot/Mastermind/commit/fe1a36c1f88973efa02e8b065dd743512e893217))*
- Full interface for quit and discard in gameboard *([14f32d7](https://github.com/FlysonBot/Mastermind/commit/14f32d79d50d980c7661b5b11cd2d038aa10cb93))*
- Gameboard fully support undo and redo interaction *([dc1f451](https://github.com/FlysonBot/Mastermind/commit/dc1f451bf7981a5a42d523995a779c2b0b45eb4d))*
- Fully support undo and redo feature *([cb8e568](https://github.com/FlysonBot/Mastermind/commit/cb8e56897ffd7de85f7cd1c169f1436539fdc3ac))*

### 🐛 Bug Fixes

- Remove colab integration *([f62e84d](https://github.com/FlysonBot/Mastermind/commit/f62e84d72d277bfbb501c3bff2851dd9f5b06e97))*
- Relative import in tests *([5cb6d3c](https://github.com/FlysonBot/Mastermind/commit/5cb6d3c92dd52f1818123fe27d9bdd7b83e21ff5))*
- Error calling update_kwargs without kwargs *([eb375a1](https://github.com/FlysonBot/Mastermind/commit/eb375a1878c6c0d7dba78b5a9e05efab51ee7205))*
- **[Breaking]** Validation need to happen before initialization *([25a1fd4](https://github.com/FlysonBot/Mastermind/commit/25a1fd4b8f57d0c0fcd5637ff25ae618890b3ff0))*
- Avoid converting non-string input to desired type (e.g. float to int) *([2bb19d9](https://github.com/FlysonBot/Mastermind/commit/2bb19d9ebcf7ab772f8fda0ebcdd40ec5f28d276))*
- Attempt to update kwargs when kwargs is undefined *([6eab4aa](https://github.com/FlysonBot/Mastermind/commit/6eab4aa2a094ec7f0e92ce2a737ccbf1565f5ca4))*
- Kwargs must be passed through constructor and neccessary kwargs must be provided *([0e0c372](https://github.com/FlysonBot/Mastermind/commit/0e0c37258cd3e909a60ba6bd860fb8207d704a24))*
- Store and validate kwargs before validating value *([acbe6e1](https://github.com/FlysonBot/Mastermind/commit/acbe6e140b5994c2250c722e91ac8e0c90263a91))*
- NameError NumberofDots *([7616710](https://github.com/FlysonBot/Mastermind/commit/7616710b25ea1cc68a5d7c6fcacfe86c49625e30))*
- __setattr__ method logic and TrueFuse FalseFuse validation logic *([5abec80](https://github.com/FlysonBot/Mastermind/commit/5abec803ceaf21dcc21812ffcf6a021b12dec22d))*
- Store return value from validate method to support string conversion *([9129ec8](https://github.com/FlysonBot/Mastermind/commit/9129ec8e87142d83b0e1552a76e41eed7155b302))*
- Should not allow direct replacing of validated attribute with value of the same validated type *([e84778b](https://github.com/FlysonBot/Mastermind/commit/e84778bb937372b9f269ce2997994b1e12759379))*
- Relative import *([044417e](https://github.com/FlysonBot/Mastermind/commit/044417e49a2ab4c6562969088fa979932ecbf63a))*
- Pass game to player during construction *([85a9ef7](https://github.com/FlysonBot/Mastermind/commit/85a9ef781a309643b78afddb9a6cd273e2fe8f68))*
- Player class hierarchy and methods *([bcebbd5](https://github.com/FlysonBot/Mastermind/commit/bcebbd5a0e0a6a2babd8f2fd74ed8645e391b2e1))*
- Win and lost message call made to the wrong player *([0aa075b](https://github.com/FlysonBot/Mastermind/commit/0aa075bf157f93adb903242e0cc28d0127b810cb))*
- Error message for ValidGuess string conversion *([5befa96](https://github.com/FlysonBot/Mastermind/commit/5befa9611e8f70c384b6d293f44777ec464f789a))*

### 🚜 Refactor

- Improve main menu ui logic and add more option *([3357e7f](https://github.com/FlysonBot/Mastermind/commit/3357e7f656a0ecfa87cdbad0a579c7187ca900b3))*
- Enhance kwargs manipulation *([9dbb6d5](https://github.com/FlysonBot/Mastermind/commit/9dbb6d5dc828fc19770fec1a061db99bbcaed22b))*
- Improve test readability *([28d1eb2](https://github.com/FlysonBot/Mastermind/commit/28d1eb2d5fbc752a8df0c0f1e0ed90c65b722c25))*
- Replace some validation models with customized confined integer *([23979b2](https://github.com/FlysonBot/Mastermind/commit/23979b212de68202c742cd2ae7ab2944a5ddc22b))*

### 📚 Documentation

- Restyle single-line docstring; fix some typo in players.py *([aa459a2](https://github.com/FlysonBot/Mastermind/commit/aa459a2a5a9b46c328f9f5e5fcb2b4bb9b7f64ea))*

### 🎨 Styling

- Reorder elements in players.py *([05e69a7](https://github.com/FlysonBot/Mastermind/commit/05e69a7b698ba2b809c4e3666ee076df48113e10))*
- Add the accessors and mutators labels back *([f549041](https://github.com/FlysonBot/Mastermind/commit/f5490410e18eb7492731e2b57b3995e77f559213))*

### 🧪 Testing

- Isolate tests to test folder *([9d6a547](https://github.com/FlysonBot/Mastermind/commit/9d6a547f6d963eff42f2b66fb7b413acff720a5e))*
- Remove unnecessary tests *([590d6dc](https://github.com/FlysonBot/Mastermind/commit/590d6dc2f7869a86e4355f63e280c73814a8af1c))*
- Add tests for new validate types *([1ef5cba](https://github.com/FlysonBot/Mastermind/commit/1ef5cba3a5b49c8f0855c708d1e36318068bf1d1))*
- Add more validation tests for confined integer *([ad4a89b](https://github.com/FlysonBot/Mastermind/commit/ad4a89b971e5651cc9c671f1b4c3071e79e814b5))*

### ⚙️ Miscellaneous Tasks

- Rename data_validation to validation *([8f05b74](https://github.com/FlysonBot/Mastermind/commit/8f05b740ca6af0a3cb48bd4e783e1acef089b98f))*

<!-- generated by git-cliff -->
