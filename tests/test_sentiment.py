# if __name__ == "__main__":
#     deepseek = DeepSeek(os.getenv("DEEPSEEK_URL"), os.getenv("DEEPSEEK_KEY"), os.getenv("OPENAI_API_KEY"))
    
#     test_inputs = [
#     # 1) Ethereum upgrade scenario (with varied comments including tags, positivity, negativity)
#     [
#         {
#             "network": "ethereum",
#             "postId": "2451",
#             "postContent": (
#                 "Ethereum developers have announced a major upgrade, 'Dencun,' aimed at reducing gas fees "
#                 "and improving scalability. This update will introduce proto-danksharding, enhancing rollups' "
#                 "efficiency. Faster transactions and lower costs are expected, making Ethereum more competitive "
#                 "with Layer 2 solutions. A roadmap has been released, and the community is discussing the "
#                 "long-term impact."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "@vitalik This is going to change the game for Ethereum, excited for the lower fees!",
#             "id": 1001,
#             "username": "CryptoFan"
#         },
#         {
#             "content": "Honestly, I'll believe it when I see it. Too many delays in the past.",
#             "id": 1002,
#             "username": "SkepticalUser"
#         },
#         {
#             "content": "GAS FEES down?? That’s all I care about, lol.",
#             "id": 1003,
#             "username": "GasRelief"
#         },
#         {
#             "content": "I think Polygon and Arbitrum are still better scaling solutions than this proto-thingy!",
#             "id": 1004,
#             "username": "Layer2King"
#         }
#     ],

#     # 2) Solana network improvements (comment mentions and short texts)
#     [
#         {
#             "network": "solana",
#             "postId": "999",
#             "postContent": (
#                 "Solana developers claim a new patch will drastically reduce the frequency of network outages. "
#                 "Dubbed 'Hypersync,' this upgrade focuses on optimizing validator communication and preventing "
#                 "congestion. The roadmap includes phased implementation across mainnet."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "Finally! My DeFi apps were getting killed by those random outages.",
#             "id": 1101,
#             "username": "DeFiWarrior"
#         },
#         {
#             "content": "Unpopular opinion: Solana is still too centralized, outages or not.",
#             "id": 1102,
#             "username": "DecentralMax"
#         },
#         {
#             "content": "I’ll wait and see. My trust in Solana is shaky at best.",
#             "id": 1103,
#             "username": "WaryWhale"
#         },
#         {
#             "content": "Hypersync is exactly what we needed. 2023 is Solana’s year!",
#             "id": 1104,
#             "username": "SunnySide"
#         },
#     ],

#     # 3) Polkadot treasury proposal (includes user tagging and sarcasm)
#     [
#         {
#             "network": "polkadot",
#             "postId": "551",
#             "postContent": (
#                 "A new proposal has been submitted to the Polkadot treasury requesting funds for a cross-chain "
#                 "DApp security initiative. The proposal outlines a plan to audit DeFi protocols building on "
#                 "Polkadot parachains, aiming to prevent exploits and bolster user trust."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "Great initiative. Security is paramount in the DeFi space.",
#             "id": 1201,
#             "username": "AuditAdvocate"
#         },
#         {
#             "content": "@GavinWood Are we sure the treasury can handle another big payout?",
#             "id": 1202,
#             "username": "ConcernedValidator"
#         },
#         {
#             "content": "Another attempt to funnel DOT out of the treasury. Right on schedule!",
#             "id": 1203,
#             "username": "SarcasticSam"
#         },
#         {
#             "content": "Is there any timeline mentioned for the audits? I can’t find it in the proposal.",
#             "id": 1204,
#             "username": "DetailSeeker"
#         }
#     ],

#     # 4) Cardano Hydra update (includes multiple languages and emojis)
#     [
#         {
#             "network": "cardano",
#             "postId": "789",
#             "postContent": (
#                 "The long-awaited Hydra scaling solution for Cardano is set to launch. It aims to enable high-"
#                 "throughput transactions, lowering fees and enhancing the user experience. Developers promise "
#                 "faster block finality and improved interoperability with other chains."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "¡Increíble! Cardano por fin se pone al día con otras blockchains. 🚀",
#             "id": 1301,
#             "username": "LatinoCrypto"
#         },
#         {
#             "content": "Just hype or real tech? Cardano is famous for taking forever.",
#             "id": 1302,
#             "username": "TimeIsMoney"
#         },
#         {
#             "content": "@CharlesHoskinson Hydra is the next big thing? I'm hopeful but also cautious.",
#             "id": 1303,
#             "username": "ADAearlyAdopter"
#         },
#         {
#             "content": "I prefer Polkadot's approach. Cardano still doesn't have many real dApps. 😑",
#             "id": 1304,
#             "username": "CrossChainFan"
#         },
#         {
#             "content": "Hydra = multi-headed solution? Let’s hope it doesn’t create more problems!",
#             "id": 1305,
#             "username": "GreekGeek"
#         }
#     ],

#     # 5) Near Protocol’s nightshade feature (extreme positivity and negativity)
#     [
#         {
#             "network": "near",
#             "postId": "321",
#             "postContent": (
#                 "Near Protocol has introduced an upgraded 'Nightshade' sharding mechanism to expand "
#                 "transaction throughput. The update reduces validator load and enables the network to "
#                 "process more smart contracts simultaneously."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "Nightshade is absolutely revolutionary! NEAR to the moon!",
#             "id": 1401,
#             "username": "MoonChaser"
#         },
#         {
#             "content": "Meh, another hype name with no substance. Been there, done that.",
#             "id": 1402,
#             "username": "Realist123"
#         },
#         {
#             "content": "If the TPS claims are true, then NEAR might be unstoppable.",
#             "id": 1403,
#             "username": "TPSTester"
#         },
#         {
#             "content": "I hate these marketing buzzwords. 'Nightshade'? Really?",
#             "id": 1404,
#             "username": "FUDMaster"
#         }
#     ],

#     # 6) Algorand ecosystem grant (very short comments, one with uppercase emphasis)
#     [
#         {
#             "network": "algorand",
#             "postId": "654",
#             "postContent": (
#                 "Algorand Foundation has announced a new grant program to support DeFi protocols. "
#                 "The initiative will offer financial and technical resources to emerging projects."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "Nice!",
#             "id": 1501,
#             "username": "ShortComment"
#         },
#         {
#             "content": "More money for rug pulls? Let's see.",
#             "id": 1502,
#             "username": "SkepticalOne"
#         },
#         {
#             "content": "ALGO’s approach to DeFi is underrated.",
#             "id": 1503,
#             "username": "Defender"
#         },
#         {
#             "content": "THIS IS EXACTLY WHAT WE NEEDED!!!",
#             "id": 1504,
#             "username": "ExcitedShout"
#         }
#     ],

#     # 7) Tron DAO announcement (includes a spammy comment and user mention)
#     [
#         {
#             "network": "tron",
#             "postId": "888",
#             "postContent": (
#                 "Tron DAO is proposing a new governance model to distribute staking rewards more fairly. "
#                 "Validators will have to meet higher requirements and maintain transparent reporting."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "Earn 100x your TRON in 24 hours! Visit my profile!!!",
#             "id": 1601,
#             "username": "SpamBot"
#         },
#         {
#             "content": "I’m tagging @justinsun here to see if he really is behind this idea.",
#             "id": 1602,
#             "username": "CuriousCat"
#         },
#         {
#             "content": "Tron keeps surprising me—maybe in a good way this time?",
#             "id": 1603,
#             "username": "SlightlyPositive"
#         },
#         {
#             "content": "No one asked for a new governance model. Tron is fine as is.",
#             "id": 1604,
#             "username": "StatusQuo"
#         }
#     ],

#     # 8) Avalanche subnet expansion (including a comment referencing another chain entirely)
#     [
#         {
#             "network": "avalanche",
#             "postId": "202",
#             "postContent": (
#                 "Avalanche Subnets will soon offer streamlined processes for deploying new blockchains. "
#                 "Developers can customize virtual machines, enabling specialized use-cases and faster finality."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "Subnets are the future, we’ll see ETH bridging to AVAX soon.",
#             "id": 1701,
#             "username": "BridgeBuilder"
#         },
#         {
#             "content": "Cool idea, but I'm all in on Cosmos. IBC is more mature than subnets.",
#             "id": 1702,
#             "username": "CosmosCrusader"
#         },
#         {
#             "content": "Can’t wait to deploy my gaming project on a custom subnet!",
#             "id": 1703,
#             "username": "GameFiGuru"
#         },
#         {
#             "content": "Yet another chain copying Polkadot's parachains? LOL.",
#             "id": 1704,
#             "username": "PolkaFan"
#         }
#     ],

#     # 9) Fantom’s gas monetization model (negative, neutral, and a mention of competitor)
#     [
#         {
#             "network": "fantom",
#             "postId": "515",
#             "postContent": (
#                 "Fantom has introduced a new gas monetization model that rewards developers based on "
#                 "the usage of their smart contracts. The approach aims to incentivize more building on Fantom."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "It’s about time devs get rewarded for high usage DApps!",
#             "id": 1801,
#             "username": "BuilderBoost"
#         },
#         {
#             "content": "Just a gimmick. Ethereum’s ecosystem is still bigger.",
#             "id": 1802,
#             "username": "ETHFever"
#         },
#         {
#             "content": "No strong opinion, but it’s an interesting experiment. Let’s see how it pans out.",
#             "id": 1803,
#             "username": "NeutralNancy"
#         },
#         {
#             "content": "I’m going to deploy a spam contract just to farm rewards, haha.",
#             "id": 1804,
#             "username": "MaliciousMeme"
#         }
#     ],

#     # 10) Cosmos shared security rollout (mix of positivity, foreign language, short negativity)
#     [
#         {
#             "network": "cosmos",
#             "postId": "3000",
#             "postContent": (
#                 "Cosmos Hub is rolling out Interchain Security, allowing smaller chains to leverage "
#                 "the security of the Cosmos Hub's validator set. This aims to reduce the barrier to "
#                 "entry for new blockchains in the ecosystem."
#             ),
#             "safeKey": "n/a"
#         },
#         {
#             "content": "Esto es increíble, un paso gigantesco para Cosmos. 🚀",
#             "id": 1901,
#             "username": "LatAmStaker"
#         },
#         {
#             "content": "Finally, new projects can focus on innovation instead of bootstrapping security.",
#             "id": 1902,
#             "username": "IBCChampion"
#         },
#         {
#             "content": "FUD: Watch them fail to deliver on time!",
#             "id": 1903,
#             "username": "ShortFuse"
#         },
#         {
#             "content": "Can’t wait to see cross-chain DeFi blow up. Let’s go!",
#             "id": 1904,
#             "username": "HopiumHolder"
#         }
#     ]
# ]

    
#     # input_text = [{'network': 'ethereum', 'postId': '2451', 'postContent': "Ethereum developers have announced a major upgrade, 'Dencun,' set to improve scalability and reduce gas fees on the network. This update will introduce proto-danksharding, an innovation that enhances rollups' efficiency. With this upgrade, users can expect faster transactions and lower costs, making Ethereum more competitive with Layer 2 solutions. The Ethereum Foundation has released a roadmap detailing the upgrade phases, and the community is actively discussing its potential impact.", 'safeKey': 'n/a'}, {'content': 'This is a much-needed update! Ethereum has been struggling with high gas fees, and this could be a game-changer.', 'id': 7890, 'username': 'CryptoHodler'}, {'content': 'How does proto-danksharding compare to other Layer 2 solutions like Optimism and Arbitrum?', 'id': 7891, 'username': 'TechEnthusiast'}, {'content': 'If Firedancer delivers as promised, Solana could truly be the fastest blockchain out there. Exciting times ahead!', 'id': 8923, 'username': 'BlockChainGuru'}, {'content': 'Solana’s network has faced downtime before. Will Firedancer solve these stability issues?', 'id': 8924, 'username': 'DeFiMaster'}]
#     for input_text in test_inputs:
#         output_positive, output_negative, output_neutral = deepseek.get_summary(str(input_text))
#         print(output_positive, output_negative, output_neutral)
    
    
    

            