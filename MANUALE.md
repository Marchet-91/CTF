# Checklist A/D

## 1) Cosa setuppare sulla VulnBox

### 1.1 Bootstrap servizi

#### 1.1.1 Preparazione Git
- [ ] Abilitare salvataggio credenziali git (`git config --global credential.helper store`).

#### 1.1.2 Discovery e startup servizi
- [ ] Cercare tutti i `docker-compose.yml` nella cartella home, quelli sono i servizi
- [ ] Per ogni servizio:
  - [ ] Segnarsi il nome del servizio e la porta che utilizza (leggere il `docker-compose.yml`)
  - [ ] Avviare ogni servizio entrando nella cartella del servizio e facendo `docker compose up -d --build`.

#### 1.1.3 Inizializzazione repository per patching rapido
- [ ] Creare repo remoto sul [server git srdnlen](https://git.srdnlen.it) per ogni servizio (o da browser o usando uno scriptino curl per automatizzare la post request)
- [ ] Entrare nella cartella del servizio e runnare questi comandi in sequenza
```bash
git init
git remote add origin https://git.srdnlen.it/srdnlen-admin/$(pwd).git
git add .
git commit -m "First commit"
git push origin main
```

### 1.2 Clonazione tool SRDNLEN
- [ ] `git clone https://git.srdnlen.it/srdnlen-admin/POBA-Firewall.git`
- [ ] `git clone https://git.srdnlen.it/srdnlen-admin/nurax.git`

### 1.3 Setup Nurax server - Valutare se metterlo su host sistemista o su vulnbox
- [ ] Entrare in `nurax/server`.
- [ ] Configurare i parametri fondamentali come durata tick, ip vulnbox, team token, password e apikey (che può coincidere con la password, per comodità).
- [ ] Avviare `docker compose up -d --build`.

### 1.4 Setup POBA firewall

#### 1.4.1 Configurazione guidata `config.toml`
- [ ] Entrare in `~/POBA-Firewall`.
- [ ] nano ./config/config.toml
- [ ] Per ogni servizio, duplicare il blocco service (lo si trova nella wiki)
  - [ ] `service_port` è la porta del servizio che ci si è segnati in precedenza.
  - [ ] Decidere `http = true/false`. Dipende se il servizio usa tcp o http
- [ ] Se usa HTTPS, impostare anche il blocco `ssl_conf`.

#### 1.4.2 Avvio e attivazione firewall
- [ ] `docker compose up -d --build` in `POBA-Firewall`.
- [ ] `docker exec poba-firewall poba-firewall start`.
- [ ] `docker exec poba-firewall poba-firewall enable-forwarding`.
- [ ] `docker exec poba-firewall poba-firewall reload`.

---

## 2) Cosa setuppare sull'host del sistemista

Qui sopra dobbiamo solo metterci Tulip. Potenzialmente anche Nurax server (potrebbe essere più sicuro, ma ricordarsi di cambiare l'IP usato dal client)

### 2.1 Setup Tulip

#### 2.1.1 Deploy Tulip
- [ ] Clonare repo `tulip` ed entrarci
- [ ] `mkdir pcaps`
- [ ] `cp .env.example .env`.

#### 2.1.2 Configurazione `.env`
- [ ] Impostare `TRAFFIC_DIR_HOST` (default `./pcaps`).
- [ ] Impostare `TICK_START` - Inserire data e ora di inizio della challenge
- [ ] Impostare `TICK_LENGTH`. - Nel caso delle gare di Gaspare, credo sia sempre 120 secondi (verificare se andavano inseriti i secondi o i millisecondi)
- [ ] Impostare `VM_IP` - `10.10.<TEAM_NUMBER>.1`
- [ ] Impostare `TEAM_ID`.

#### 2.1.3 Configurazione helper API
- [ ] Aggiornare blocco `helper = '''...'''` in `services/api/configurations.py`.
- [ ] Inserire tutti i servizi helper necessari (IP, porta, nome). (fare attenzione all'ip, altrimenti Tulip mostra Unknown)

#### 2.1.4 Avvio stack Tulip
- [ ] Eseguire `ssh -q root@10.60.{NUMERO_TEAM}.1 "tcpdump -i game -U -s 0 -w - port 1337 or port 80 or port 5000 or port 5555" | tcpdump -U -r - -G 180 -w "./pcaps/traffic_%H:%M:%S.pcap"` sostituendo 1337,80,5000 e 5555 con le porte dei servizi.
- [ ] Eseguire `docker compose up -d --build` in `tulip`.

#### 2.1.5 Accesso dashboard
- [ ] `echo "Aprite Tulip a questo URL: http://$(ifconfig | grep "inet 10.81" | awk '{print $2}'):3000"`
- [ ] Condividere URL Tulip con il team: `http://<IP_SISTEMISTA>:3000`.

---

## 3) Durante la gara

### 3.1 Routine ogni tick
- [ ] Verificare stato container critici (`docker ps`) su VulnBox e sistemista.
- [ ] Verificare che i servizi di gara rispondano, guardando la dashboard e stando attenti su discord se si viene avvertiti che un servizio è down (basta una sola lucina rossa e si perdono i punti per quel round per quel servizio).
- [ ] Verificare stream PCAP attivo e nuovi file in `pcaps/`.
- [ ] Verificare POBA in esecuzione e forwarding attivo.

### 3.2 Monitoraggio difensivo
- [ ] Controllare log POBA per trigger sospetti:
  - [ ] `docker logs -f poba-firewall`
  - [ ] oppure solo attivazioni dei filtri (aggiungere ` | grep "WARNING"`).
- [ ] Segnalare al team exploit avversari osservati.

### 3.3 Hardening rapido filtri POBA
- [ ] Editare filtro inbound/outbound del servizio impattato (`nano firewall/filters/<service_name>/<service_name>_in.py`) . (nel 90% dei casi bisogna usare quelli inbound, ma se si è sicuri di rispettare le regole, esplorare anche filtri out)
- [ ] IMPORTANTE: Dopo aver editato il file, ricaricare regole (`docker run poba-firewall poba-firewall reload`). 
- [ ] Monitorare immediatamente log per confermare mitigazione.

### 3.4 Come patchare
- [ ] Entrare nel repository del servizio compromesso su VulnBox.
```bash
docker compose down
git pull
docker compose up -d --build
```
- [ ] Validare nuovamente disponibilita' e scorecheck.

---

## 4) Comandi rapidi (riferimento)

### 4.1 Nurax (invio exploit)
- [ ] Usare token Nurax e lanciare exploit:

```bash
NURAX_TOK="Artoor0" # Token di esempio, non riusarlo lol
nurax -u http://10.60.$NUMERO_TEAM.1:3000 -t "$NURAX_TOK" -e NOME_EXPLOIT -s service -f FILE_EXPLOIT.py
```

### 4.2 POBA logs

```bash
docker logs -f poba-firewall 2>&1 | grep "WARNING"
```


---

## 5) Troubleshooting checklist

### 5.1 Deploy/SSH fallisce
- [ ] Verificare raggiungibilita' `10.60.<TEAM>.1`.
- [ ] Verificare credenziali SSH/root.
- [ ] Verificare che firewall locale non blocchi SSH.

### 5.2 Errori in compose/build
- [ ] Verificare spazio disco e stato Docker daemon.
- [ ] Rieseguire build con log completo.
- [ ] Verificare conflitti porte tra servizi.

### 5.3 Nessun servizio scoperto da TUI POBA
- [ ] Verificare presenza `docker-compose.yml` in home VulnBox.
- [ ] Verificare che esista almeno una mappatura porte `host:container`.

### 5.4 Tulip non mostra dati
- [ ] Verificare che i file PCAP vengano generati in `pcaps/`.
- [ ] Verificare valori `.env` (`TRAFFIC_DIR_HOST`, `VM_IP`, `TEAM_ID`).
- [ ] Verificare helper services in `services/api/configurations.py`.

### 5.5 Filtro POBA modificato ma effetto nullo
- [ ] Verificare che il file `_in.py`/`_out.py` corretto sia stato editato.
- [ ] Verificare reload regole riuscito.
- [ ] Verificare log warning dopo reload.