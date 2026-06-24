# 参考文献Abstract集

## 目次
[目次](#目次)
[参考文献](#参考文献)
[Abstruct](#abstract)

---
## 参考文献
日付はyyyy/MM

- [Inconsistent Tokenizations Cause Language Models to be Perplexed by Japanese Grammar](./2025.acl-short.75.pdf)
  - Andrew Gambardella, Takeshi Kojima, Yusuke Iwasawa, Yutaka Matsuo
  - 2025/07
- [Improbable Bigrams Expose Vulnerabilities of Incomplete Tokens in Byte-Level Tokenizers](2025.emnlp-main.919.pdf)
  - Eugene Jang, Kimin Lee, Jin-Woo Chung, Keuntae Park, Seungwon Shin
  - 2025/11
- [How does a Language-Specific Tokenizer affect LLMs?](./2502.12560v2.pdf)
  - Jean Seo, Jaeyoon Kim, SungJoo Byun, Hyopil Shin
  - 2025/02
- [Chinese Language Is Not More Efficient Than English in Vibe Coding: A Preliminary Study on Token Cost and Problem-Solving Rate](./2604.14210v1.pdf)
  - Simiao Ren, Xingyu Shen, Yuchen Zhou, Dennis (Tsang)Ng, Ankit Raj
  - 2026/04

---
## Abstract

### Inconsistent Tokenizations Cause Language Models to be Perplexed by Japanese Grammar

```text
Typical methods for evaluating the performance of language models evaluate their ability to answer questions accurately. These evaluation metrics are acceptable for determining the extent to which language models can understand and reason about text in a general sense, but fail to capture nuanced capabilities, such as the ability of language models to recognize and obey rare grammar points, particularly in languages other than English. We measure the perplexity of language models when confronted with the “first person psych predicate restriction” grammar point in Japanese. Weblab is the only tested open source model in the 7-10B parameter range which consistently assigns higher perplexity to ungrammatical psych predicate sentences than grammatical ones. We give evidence that Weblab’s uniformly bad tokenization is a possible root cause for its good performance, and show that Llama 3’s perplexity on grammatical psych predicate sentences can be reduced by orders of magnitude (28x difference) by restricting test sentences to those with uniformly well-behaved tokenizations. We show in further experiments on machine translation tasks that language models will use alternative grammar patterns in order to produce grammatical sentences when tokenization issues prevent the most natural sentence from being output.
```

---
### Improbable Bigrams Expose Vulnerabilities of Incomplete Tokens in Byte-Level Tokenizers
```text
Tokenization is a crucial step that bridges human-readable text with model-readable discrete tokens. However, recent studies have revealed that tokenizers can be exploited to elicit unwanted model behaviors. In this work, we investigate incomplete tokens, i.e., undecodable tokens with stray bytes resulting from byte-level byte-pair encoding (BPE) tokenization. We hypothesize that such tokens are heavily reliant on their adjacent tokens and are fragile when paired with unfamiliar tokens. To demonstrate this vulnerability, we introduce improbable bigrams: out-of-distribution combinations of incomplete tokens designed to exploit their dependency. Our experiments show that improbable bigrams are significantly prone to hallucinatory behaviors. Surprisingly, the same phrases have drastically lower rates of hallucination (90% reduction in Llama3.1) when an alternative tokenization is used. We caution against the potential vulnerabilities introduced by byte-level BPE tokenizers, which may introduce blind spots to language models.
```

---
### How does a Language-Specific Tokenizer affect LLMs?
```text
The necessity of language-specific tokenizers intuitively appears crucial for effective natural language processing, yet empirical analyses on their significance and underlying reasons are lacking. This study explores how language-specific tokenizers influence the behavior of Large Language Models predominantly trained with English text data, through the case study of Korean. The research unfolds in two main stages: (1) the development of a Korean-specific extended tokenizer and (2) experiments to compare models with the basic tokenizer and the extended tokenizer through various Next Token Prediction tasks. Our in-depth analysis reveals that the extended tokenizer decreases confidence in incorrect predictions during generation and reduces cross-entropy in complex tasks, indicating a tendency to produce less nonsensical outputs. Consequently, the extended tokenizer provides stability during generation, potentially leading to higher performance in downstream tasks.
```

---
### Chinese Language Is Not More Efficient Than English in Vibe Coding: A Preliminary Study on Token Cost and Problem-Solving Rate
```text
A claim has been circulating on social media and practitioner forums that Chinese prompts are more token-efficient than English for LLM coding tasks, potentially reducing costs by up to 40\%. This claim has influenced developers to consider switching to Chinese for ``vibe coding'' to save on API costs. In this paper, we conduct a rigorous empirical study using SWE-bench Lite, a benchmark of software engineering tasks, to evaluate whether this claim of Chinese token efficiency holds up to scrutiny. Our results reveal three key findings: First, the efficiency advantage of Chinese is not observed. Second, token cost varies by model architecture in ways that defy simple assumptions: while MiniMax-2.7 shows 1.28x higher token costs for Chinese, GLM-5 actually consumes fewer tokens with Chinese prompts. Third, and most importantly, we found that the success rate when prompting in Chinese is generally lower than in English across all models we tested. We also measure cost efficiency as expected cost per successful task -- jointly accounting for token consumption and task resolution rate. These findings should be interpreted as preliminary evidence rather than a definitive conclusion, given the limited number of models evaluated and the narrow set of benchmarks tested due to resource constraints; they indicate that language effects on token cost are model-dependent, and that practitioners should not expect cost savings or performance gains just by switching their prompt language to Chinese.
```