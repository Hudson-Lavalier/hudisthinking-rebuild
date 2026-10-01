import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import CustomPage, NavigationItem

# 1. Terminal Trader Privacy Policy (verbatim from WordPress SQL ID 780)
tt_privacy_body = """*Effective Date: August 17, 2026*

This Privacy Policy describes how **Terminal Trader**, developed and published by **HudIsThinking** ("we," "us," or "our"), handles information when you use the game.

Terminal Trader is designed to operate primarily as an offline game. It does not require a user account, does not contain advertising, and does not intentionally collect or transmit personal information to HudIsThinking.

---

### 1. Information We Collect

Terminal Trader does not intentionally collect personal information from players.

The game does not require you to provide your name, email address, phone number, physical address, location, contacts, payment information, advertising identifier, account credentials, or other personally identifying information in order to play.

Terminal Trader also does not use a HudIsThinking account system or player registration system.

---

### 2. Game and Save Data

Terminal Trader creates and stores gameplay information locally on your device so that your progress can be saved and restored between sessions.

This local game data may include information such as:
- cash and portfolio values
- stock holdings and investments
- bonds
- business ownership and management
- real estate
- managers and analysts
- upgrades and purchases
- achievements
- tutorial progress
- game settings
- in-game messages
- unlock and progression state
- event state
- other information required to restore your game session

This information is used only as game-state data. It is not used to create a personal profile about you.

---

### 3. Local Storage

Terminal Trader stores normal save information locally on your device.

On Android, the game uses application storage provided through the Android operating system and the Capacitor filesystem environment. On supported desktop versions, game data may also be stored using local application storage appropriate to that platform.

HudIsThinking does not operate a remote database containing normal Terminal Trader save files.

---

### 4. Save Export and Import

Terminal Trader may allow you to export or import save data.

An exported save contains information necessary to recreate your game state. Exporting a save does not automatically transmit the file to HudIsThinking.

If you choose to copy, upload, email, back up, or otherwise share an exported save file, that action is controlled by you and by any third-party service you choose to use.

Imported save files are processed locally by Terminal Trader in order to restore the supplied game state.

---

### 5. Internet Connectivity

Terminal Trader does not require a HudIsThinking account or a connection to HudIsThinking servers for normal gameplay.

The game is not designed to transmit your portfolio activity, achievements, save state, gameplay decisions, or other normal game progress to HudIsThinking.

Terminal Trader does not currently provide a HudIsThinking-operated cloud save service, multiplayer service, or online player account system.

---

### 6. Analytics, Advertising, and Tracking

Terminal Trader does not intentionally use analytics services, behavioral tracking systems, or advertising networks.

We do not intentionally track which features you use, which investments you make, how long you play, which achievements you earn, or which hidden content you discover.

Terminal Trader does not contain third-party advertising and does not intentionally collect advertising identifiers for personalized advertising or behavioral profiling.

---

### 7. Third-Party Software

Terminal Trader uses software libraries and platform components necessary to package and operate the game.

The Android version uses technologies including Android system components, Capacitor, and the Capacitor Filesystem plugin. These components are used to operate the application and support local file storage.

HudIsThinking does not intentionally configure these components to collect personal information, analytics, advertising information, or gameplay tracking information.

---

### 8. Sharing and Sale of Information

HudIsThinking does not intentionally sell, rent, trade, or share personal information obtained through Terminal Trader.

Because normal gameplay and save information remain on the user's device, HudIsThinking does not normally receive that information in the first place.

---

### 9. Data Retention

Terminal Trader's normal game data remains stored locally on your device for as long as the application or operating system retains it.

HudIsThinking does not determine the retention period for local save files because those files are not normally stored on HudIsThinking servers.

---

### 10. Deleting Your Data

You may remove locally stored Terminal Trader game data using available game reset functionality, by clearing the application's storage through your device settings, or by uninstalling the game.

Exported save files that you have manually stored elsewhere must be deleted separately from the location where you saved them.

Because Terminal Trader does not normally maintain a remote player account or remote save database, there is generally no remote Terminal Trader account data for HudIsThinking to delete.

---

### 11. Data Security

Terminal Trader is designed to minimize privacy risk by keeping normal gameplay data on the player's device rather than transmitting it to HudIsThinking.

No method of electronic storage can be guaranteed to be completely secure. Users are responsible for protecting access to their devices and any save files they choose to export or share.

---

### 12. Google Play and Platform Services

If you obtain Terminal Trader through Google Play or another digital distribution platform, certain information relating to your store account, purchases, downloads, or platform usage may be processed by that platform independently of Terminal Trader.

HudIsThinking does not receive your complete payment-card information through Terminal Trader.

Information handled directly by Google Play or another platform is governed by that platform's own privacy policy and terms.

---

### 13. Children's Privacy

Terminal Trader does not intentionally collect personal information from children or adults through normal gameplay.

The game does not require players to submit personal information in order to play.

---

### 14. Changes to This Privacy Policy

We may update this Privacy Policy if Terminal Trader changes in a way that affects how information is accessed, stored, collected, used, or shared.

When this policy is updated, the Effective Date shown at the top of this page will be revised.

---

### 15. Contact

If you have questions about this Privacy Policy or Terminal Trader's privacy practices, you may contact:

- **Developer:** HudIsThinking LLC
- **Game:** Terminal Trader
- **Website:** [hudisthinking.com](https://hudisthinking.com)
- **Email:** Support@hudisthinking.com
"""

# 2. Terminal Trader Terms of Service
tt_terms_body = """*Effective Date: August 17, 2026*

These Terms of Service ("Terms") govern your download, installation, access, and use of the software game **Terminal Trader** ("Game"), developed and published by **HudIsThinking LLC** ("HudIsThinking," "we," "us," or "our").

By downloading, installing, or playing Terminal Trader, you agree to be bound by these Terms. If you do not agree to these Terms, do not install or play the Game.

---

### 1. License Grant

Subject to your compliance with these Terms, HudIsThinking LLC grants you a limited, non-exclusive, non-transferable, revocable license to download, install, and execute one copy of Terminal Trader on a personal device solely for your personal, non-commercial entertainment purposes.

---

### 2. Intellectual Property Rights

All rights, titles, and interests in and to Terminal Trader—including but not limited to source code, binary executables, interface designs, game mechanics, text, economic algorithms, audiovisual elements, logos, and trademarks—are and will remain the exclusive property of HudIsThinking LLC and Hudson Lavalier.

You may not:
- Reverse engineer, decompile, disassemble, or attempt to derive the source code of the Game, except to the extent permitted by applicable law.
- Modify, adapt, translate, or create derivative works based upon the Game.
- Sell, rent, lease, sublicense, distribute, or commercially exploit the Game or any part thereof without prior express written consent from HudIsThinking LLC.
- Remove, alter, or obscure any copyright, trademark, or other proprietary rights notices contained in the Game.

---

### 3. Gameplay, Save Data, and Local Storage

Terminal Trader operates primarily as a local, offline simulation. 

- All gameplay decisions, financial portfolios, stock trades, achievements, and game saves are stored locally on your device.
- You are solely responsible for backing up, maintaining, or transferring your exported save files. HudIsThinking LLC does not maintain remote backup copies of your local game saves and is not liable for data loss resulting from hardware failure, device resets, or application uninstallation.

---

### 4. Third-Party Platforms

If you download Terminal Trader through Google Play or another digital storefront, your purchase, download, and store account are also subject to the applicable storefront terms and conditions. In the event of a conflict between platform terms and these Terms, the platform terms will govern with respect to store transactions.

---

### 5. Disclaimer of Warranties

Terminal Trader is provided on an **"AS IS"** and **"AS AVAILABLE"** basis, without warranties of any kind, either express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.

HudIsThinking LLC does not warrant that the Game will be error-free, uninterrupted, compatible with all devices or operating system versions, or that defects will be immediately corrected.

---

### 6. Limitation of Liability

To the maximum extent permitted by applicable law, in no event shall HudIsThinking LLC, its officers, directors, employees, or licensors be liable for any indirect, incidental, special, consequential, or punitive damages, including loss of data, loss of profits, device damage, or business interruption, arising out of or in connection with your access to or use of (or inability to use) Terminal Trader.

---

### 7. Termination

Your rights under these Terms will terminate automatically without notice if you fail to comply with any provision of these Terms. Upon termination, you must cease all use of Terminal Trader and delete all copies of the Game from your devices.

---

### 8. Changes to These Terms

We reserve the right to revise or update these Terms at any time. When changes are made, the Effective Date at the top of these Terms will be updated. Continued use of the Game following notice of revisions constitutes your acceptance of the amended Terms.

---

### 9. Governing Law

These Terms shall be governed by and construed in accordance with the laws of the State of Florida and the United States of America, without regard to conflict of law principles.

---

### 10. Contact

For inquiries regarding these Terms of Service or Terminal Trader, please contact:

- **Developer:** HudIsThinking LLC
- **Game:** Terminal Trader
- **Website:** [hudisthinking.com](https://hudisthinking.com)
- **Email:** Support@hudisthinking.com
"""

# 3. HudIsThinking Site Privacy Policy
site_privacy_body = """*Effective Date: August 17, 2026*

This Privacy Policy explains how **HudIsThinking LLC** ("HudIsThinking," "we," "us," or "our") manages information collected through our official website located at **hudisthinking.com** ("Site"), which serves as a personal archive of philosophical arguments, written treatises, software projects, and digital works.

---

### 1. Minimal Information Collection

HudIsThinking is committed to user privacy. We do not require visitors to register an account, log in, or provide personal identification to browse our philosophical treatises, projects, or articles.

We do not sell, rent, or trade your personal information to third parties or advertising brokers.

---

### 2. Server Logs and Technical Data

When you access our Site, our web servers and host infrastructure (Google Cloud Run) may automatically process standard technical request information, including:
- Your IP address
- Browser type and operating system
- Pages visited, referral source, and timestamps of access
- HTTP request status codes

This standard server log information is used strictly to maintain site reliability, prevent abuse or denial-of-service attacks, and troubleshoot server performance. It is not used to build individual user tracking profiles.

---

### 3. Cookies and Local Storage

The main HudIsThinking archive does not employ third-party advertising cookies or cross-site tracking pixels. 

Standard session cookies may be utilized solely for technical website functionality (such as administrative authentication for authorized editors and security headers).

---

### 4. Software Downloads and External Platforms

Our Site hosts download links and project documentation for independent software, games, and tools (such as *Terminal Trader* and *Desktop Buddy Companion*).

- Downloads directly hosted on our domain are delivered securely without telemetry trackers embedded in the transfer.
- External links (such as Google Play, GitHub, or our interactive platform HudIsThinking Connect) are governed by their respective platforms' privacy policies and terms of service.

---

### 5. Third-Party Links

Our Site contains links to external domains, academic papers, and related platforms. We are not responsible for the privacy policies or practices of external websites. We encourage you to review the privacy documentation of any external sites you visit.

---

### 6. Children's Privacy

Our website provides educational, philosophical, and software material and does not knowingly collect personal identifiable information from children under the age of 13.

---

### 7. Data Security

We implement reasonable technical safeguards, including HTTPS SSL/TLS encryption across all site traffic, to protect information transmitted to and from our site.

---

### 8. Updates to This Policy

We may update this Privacy Policy from time to time to reflect operational, legal, or regulatory changes. The "Effective Date" at the top of this document indicates when the policy was last revised.

---

### 9. Contact Us

If you have any questions or feedback regarding this Privacy Policy, please contact:

- **Entity:** HudIsThinking LLC
- **Website:** [hudisthinking.com](https://hudisthinking.com)
- **Email:** Support@hudisthinking.com
"""

# 4. HudIsThinking Site Terms of Service
site_terms_body = """*Effective Date: August 17, 2026*

These Terms of Service ("Terms") govern your access to and use of the website located at **hudisthinking.com** ("Site"), owned and operated by **HudIsThinking LLC** ("HudIsThinking," "we," "us," or "our").

By accessing or browsing this Site, you agree to comply with and be bound by these Terms. If you do not agree to these Terms, you should not access or use this Site.

---

### 1. Purpose and Content

HudIsThinking is a digital repository and intellectual archive featuring:
- Philosophical arguments, essays, and formal metaphysical treatises authored by Hudson Lavalier.
- Software works, game releases, and interactive tools developed under HudIsThinking LLC.
- Community portals and links to dialectical platforms.

The writings and content published here are provided for contemplation, critical study, education, and philosophical inquiry.

---

### 2. Intellectual Property Rights

Unless otherwise explicitly noted, all intellectual property on this Site—including written treatises, articles, argument structures, software code, graphic artwork, UI design, logos, and audiovisual assets—is the property of HudIsThinking LLC and Hudson Lavalier and is protected by United States and international copyright, trademark, and intellectual property laws.

- **Permitted Study & Citation:** You may read, study, cite, and reference excerpts from our philosophical treatises in academic or educational contexts, provided full attribution is clearly given to HudIsThinking and the author.
- **Restrictions:** You may not systematically scrape, reproduce, redistribute, re-license, or sell the text, manuscripts, or software binaries from this Site for commercial gain without express written consent from HudIsThinking LLC.

---

### 3. Software Downloads

Software binaries, game archives, and companion tools provided for download through this Site are licensed under their respective end-user license agreements and terms of service. Downloading any software from this site implies agreement to the specific terms associated with that program.

---

### 4. Acceptable Use

You agree not to use the Site to:
- Violate any applicable local, state, national, or international law.
- Interfere with, disrupt, or compromise the security or infrastructure of the Site, servers, or networks.
- Probe, scan, or test the vulnerability of the system without authorization.
- Transmit malicious code, viruses, or automated scraping scripts designed to overwhelm server resources.

---

### 5. Disclaimer of Warranties

The Site and all materials, software downloads, and information contained herein are provided on an **"AS IS"** and **"AS AVAILABLE"** basis without warranties of any kind, either express or implied.

HudIsThinking LLC makes no representations or warranties that the Site will be uninterrupted, error-free, secure, or free from viruses or other harmful components.

---

### 6. Limitation of Liability

To the fullest extent permitted by applicable law, in no event shall HudIsThinking LLC, Hudson Lavalier, or any associates be liable for any direct, indirect, incidental, consequential, special, or punitive damages arising out of your access to, use of, or inability to use this Site or any software downloaded through it.

---

### 7. Links to External Sites

The Site may contain links to third-party websites (such as external debate portals, platforms, or repositories). HudIsThinking LLC has no control over and assumes no responsibility for the content, privacy practices, or terms of third-party platforms.

---

### 8. Governing Law

These Terms are governed by and construed in accordance with the laws of the State of Florida and the United States of America, without regard to its conflict of law provisions.

---

### 9. Modifications

HudIsThinking LLC reserves the right to modify or replace these Terms at any time. Your continued use of the Site following the posting of any changes constitutes acceptance of those revisions.

---

### 10. Contact Information

If you have questions regarding these Terms of Service, please contact:

- **Entity:** HudIsThinking LLC
- **Website:** [hudisthinking.com](https://hudisthinking.com)
- **Email:** Support@hudisthinking.com
"""

pages_to_create = [
    {
        'title': 'Terminal Trader Privacy Policy',
        'slug': 'terminal-trader-privacy-policy',
        'content': tt_privacy_body,
        'meta_description': 'Official Privacy Policy for the Terminal Trader simulation game developed by HudIsThinking LLC.',
    },
    {
        'title': 'Terminal Trader Terms of Service',
        'slug': 'terminal-trader-terms-of-service',
        'content': tt_terms_body,
        'meta_description': 'Official Terms of Service and End User License Agreement for Terminal Trader by HudIsThinking LLC.',
    },
    {
        'title': 'Privacy Policy',
        'slug': 'privacy-policy',
        'content': site_privacy_body,
        'meta_description': 'Privacy Policy for the official HudIsThinking archive website and digital publications.',
    },
    {
        'title': 'Terms of Service',
        'slug': 'terms-of-service',
        'content': site_terms_body,
        'meta_description': 'Official Terms of Service for browsing, citing, and accessing HudIsThinking LLC.',
    },
]

for pdata in pages_to_create:
    obj, created = CustomPage.objects.update_or_create(
        slug=pdata['slug'],
        defaults={
            'title': pdata['title'],
            'content': pdata['content'],
            'meta_description': pdata['meta_description'],
            'is_published': True,
            'show_featured_image': False,
        }
    )
    status = "Created" if created else "Updated"
    print(f"[{status}] CustomPage: {obj.title} -> /page/{obj.slug}/ & /{obj.slug}/")

# Now ensure the footer has links to Privacy Policy and Terms of Service
# Let's inspect current footer items and append Privacy Policy and Terms of Service
footer_links = [
    ('Privacy Policy', '/privacy-policy/', 6),
    ('Terms of Service', '/terms-of-service/', 7),
]

for label, url, order in footer_links:
    item, created = NavigationItem.objects.get_or_create(
        label=label,
        location='footer',
        defaults={'url': url, 'order': order, 'is_active': True, 'open_in_new_tab': False}
    )
    if not created:
        item.url = url
        item.order = order
        item.is_active = True
        item.save()
    print(f"[Footer Link] {item}")
