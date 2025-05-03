const { createApp, ref } = Vue;

const DecryptForm = {
  template: `
    <div class="decryptor">
      <h1>RSA Decryptor Tool</h1>
      <form @submit.prevent="submitForm" enctype="multipart/form-data">
        <div class="form-group">
          <label>Private Key (PEM):</label>
          <input type="file" ref="keyInput" accept=".pem" required>
        </div>
        <div class="form-group">
          <label>Encrypted File:</label>
          <input type="file" ref="secretInput" required>
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Decrypting...' : 'Decrypt' }}
        </button>
      </form>

      <div v-if="result" class="result">
        <h3>Decrypted Result:</h3>
        <pre>{{ result }}</pre>
      </div>

      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>
  `,
  setup() {
    const keyInput = ref(null);
    const secretInput = ref(null);
    const result = ref('');
    const error = ref('');
    const loading = ref(false);

    const submitForm = async () => {
      error.value = '';
      result.value = '';
      loading.value = true;

      const formData = new FormData();
      formData.append('key', keyInput.value.files[0]);
      formData.append('secret', secretInput.value.files[0]);

      try {
        const response = await fetch('/decypher', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const err = await response.json();
          throw new Error(err.detail || 'Decryption failed');
        }

        const data = await response.json();
        result.value = data.result;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    };

    return { keyInput, secretInput, result, error, loading, submitForm };
  }
};

createApp({
  components: { DecryptForm }
}).mount('#app');